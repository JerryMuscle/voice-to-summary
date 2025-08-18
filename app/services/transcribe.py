import numpy as np
import soundfile as sf
import torch
import math
from concurrent.futures import ThreadPoolExecutor
from transformers import pipeline
from services.summarizer import Summarizer

class AudioTranscriber:
    def __init__(self):
        """
        文字起こしモデルの初期化

        """
        self.summarize = Summarizer()
        #  kotoba-whisperのモデル設定
        model_id = "kotoba-tech/kotoba-whisper-v2.0"
        torch_dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        # GPUで処理できるように
        device = "mps" if torch.backends.mps.is_available() else "cpu"

        # モデルロード
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model_id,
            torch_dtype=torch_dtype,
            device=device
        )

        self.generate_kwargs = {
            "language": "ja", 
            "task": "transcribe", 
            "return_timestamps": True,
            "temperature": 0.3,
            "no_repeat_ngram_size": 3,
            "repetition_penalty": 1.2
        }

    def transcribe_segment(self, segment_audio, sample_rate):
        """
        セグメントごとの録音データを文字起こし
        
        Args:
            segment_audio:セグメントされた音声データ(60s)
        """
        result = self.pipe({"array": segment_audio, "sampling_rate": sample_rate}, generate_kwargs=self.generate_kwargs)
        return result["text"]

    def transcribe_from_array(self, audio_data: np.ndarray, sample_rate: int, segment_sec=60, max_workers=2) -> str:
        """
        NumPy配列の音声データを30秒のセグメントごとに文字起こし⇨結果を結合⇨要約の実施

        Args:
            audio_data (np.ndarray): 録音された音声データ。
            sample_rate (int): 音声データのサンプリングレート。

        Returns:
            str: 文字起こしされた⇨要約されたテキスト。
        """        
        mono_audio_data = convert_to_mono(audio_data)
        normalized_audio = normalize_audio(mono_audio_data)

        segment_len = segment_sec * sample_rate
        num_segments = math.ceil(len(normalized_audio) / segment_len)

        # セグメントごとに分割して文字起こし
        segments = []
        for i in range(num_segments):
            start = i * segment_len
            end = min((i + 1) * segment_len, len(normalized_audio))
            segments.append(normalized_audio[start:end])

        texts = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(self.transcribe_segment, seg, sample_rate) for seg in segments]
            for future in futures:
                texts.append(future.result())

        # 医学用語の補正
        corrected_text = self.summarize.correct_medical_terms(texts)
        print("要約を開始します")
        summrize_result  = self.summarize.summarize_text(corrected_text)
        print("要約終了")
        return summrize_result
    
def convert_to_mono(audio_array):
    """
        ステレオ（2ch）→ モノラル（1ch）に変換する関数
            2chは左右の音をそれぞれ取得、1chは全体で同じ音
            [ [L1, R1], [L2, R2], ... ]⇨[ M1, M2, M3, ... ]にするイメージ
    """
    if len(audio_array.shape) > 1 and audio_array.shape[1] == 2:
        audio_array = np.mean(audio_array, axis=1, dtype=np.float32)
    return audio_array.squeeze().astype(np.float32)

def normalize_audio(audio: np.ndarray) -> np.ndarray:
    """
        音声データの正規化
    """
    
    max_val = np.max(np.abs(audio))
    return audio / max_val if max_val > 0 else audio