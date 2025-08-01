import whisper
import numpy as np
import soundfile as sf
import torch
from transformers import pipeline
from services.summarizer import summarize_text

class AudioTranscriber:
    def __init__(self):
        """
        文字起こしモデルの初期化
        Whisper: 英語用
        kotoba-whisper-v2.0: 日本語用
        
        Args:
            model_name (str): 使用するWhisperモデルの種類
              ("tiny", "base", "small", "medium", "large")。
        """
        # TODO: whisperのモデルサイズをguiで選べるようにする
        # model_name="base"
        # self.model = whisper.load_model(model_name)

        #  kotoba-whisperのモデル設定
        model_id = "kotoba-tech/kotoba-whisper-v2.0"
        torch_dtype = torch.bfloat16 if torch.cuda.is_available() else torch.float32
        device = "cuda:0" if torch.cuda.is_available() else "cpu"

        # モデルロード
        self.pipe = pipeline(
            "automatic-speech-recognition",
            model=model_id,
            torch_dtype=torch_dtype,
            device=device
        )

    def transcribe_from_array(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """
        NumPy配列の音声データを文字起こしします。

        Args:
            audio_data (np.ndarray): 録音された音声データ。
            sample_rate (int): 音声データのサンプリングレート。

        Returns:
            str: 文字起こしされたテキスト。
        """        
        # Whisper用で文字起こし
        # result = self.model.transcribe(temp_filename, fp16=False)

        generate_kwargs = {
            "language": "ja", 
            "task": "transcribe", 
            "return_timestamps": True  # 長い音声対応（タイムスタンプ付き）
        }
        mono_audio_data = convert_to_mono(audio_data)
        normalized_audio = normalize_audio(mono_audio_data)
        result = self.pipe({"array": normalized_audio, "sampling_rate": sample_rate}, generate_kwargs=generate_kwargs)
        # 要約処理
        summrize_result  = summarize_text(result["text"])

        return summrize_result
    
# ステレオ（2ch）→ モノラル（1ch）に変換する関数
def convert_to_mono(audio_array):
    """
        2chは左右の音をそれぞれ取得、1chは全体で同じ音
        [ [L1, R1], [L2, R2], ... ]⇨[ M1, M2, M3, ... ]にするイメージ

        この変換で処理時間が伸びてるのでは？？
        TODO:処理速度を比較する
            1. 音声データ.wavから文字起こしする
            2. Black Holeで最初から1chで録音できないか調べる→できたら実行
            3. その他の方法
    """
    if len(audio_array.shape) > 1 and audio_array.shape[1] == 2:
        audio_array = np.mean(audio_array, axis=1, dtype=np.float32)  # ステレオをモノラル化
    return audio_array.squeeze().astype(np.float32)

# 音声の正規化
def normalize_audio(audio: np.ndarray) -> np.ndarray:
    max_val = np.max(np.abs(audio))
    return audio / max_val if max_val > 0 else audio