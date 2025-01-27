import whisper
import numpy as np
import soundfile as sf

class AudioTranscriber:
    def __init__(self, model_name="base"):
        """
        Whisperモデルを初期化します。
        
        Args:
            model_name (str): 使用するWhisperモデルの種類
              ("tiny", "base", "small", "medium", "large")。
        """
        # TODO: whisperのモデルサイズをguiで選べるようにする
        self.model = whisper.load_model(model_name)

    def transcribe_from_array(self, audio_data: np.ndarray, sample_rate: int) -> str:
        """
        NumPy配列の音声データを文字起こしします。

        Args:
            audio_data (np.ndarray): 録音された音声データ。
            sample_rate (int): 音声データのサンプリングレート。

        Returns:
            str: 文字起こしされたテキスト。
        """
        # NumPy配列をWAVファイル形式に変換(文字起こしのための一時的なもの)
        # こうしたらリアルタイムで文字起こしできない？？一回一回ファイル作ってたら処理速度遅くなりそう
        temp_filename = "temp_audio.wav"
        sf.write(temp_filename, audio_data, sample_rate)
        
        # Whisperで文字起こし
        result = self.model.transcribe(temp_filename, fp16=False)
        return result["text"]

    def transcribe_from_file(self, file_path: str) -> str:
        """
        WAVファイルから文字起こしを行います。

        Args:
            file_path (str): 音声ファイルのパス。

        Returns:
            str: 文字起こしされたテキスト。
        """
        result = self.model.transcribe(file_path, fp16=False)
        return result["text"]