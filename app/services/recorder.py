import sounddevice as sd
import numpy as np
import wave
import threading

class Recorder:
    def __init__(self):
            """
            Args:
                sample_rate (int): サンプリングレート (Hz)。
                    TODO: gui_appから自分で設定できるようにする
                channels (int): チャネル数 (モノラル = 1)。
            """
            self.sample_rate = 44100
            self.channels = 2
            self.is_recording = False
            self.audio_buffer = []
            self._thread = None

    def start_audio_capture(self):
        """
        システム音声の音声取得を開始する。
        """
        if self.is_recording:
            print("既に音声取得中です。")
            return

        self.is_recording = True
        self.audio_buffer = []
        print("音声取得を開始しました...")

        def record():
            # BlackHoleを指定した入力ストリームを開く
            with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, dtype='float32',
                                device="BlackHole 2ch", callback=self.audio_callback):
                while self.is_recording:
                    sd.sleep(100)

        # 録音スレッドを開始
        self._thread = threading.Thread(target=record, daemon=True)
        self._thread.start()

    def audio_callback(self, indata, frames, time, status):
        """
        音声データを録音バッファに追加するコールバック関数。

        Args:
            indata (np.ndarray): 取得した音声たデータ。
            frames (int): フレーム数。
            time (CData): 時間情報。
            status (CallbackFlags): ステータス情報。
        """
        if status:
            print(f"録音中にエラーが発生しました: {status}")
        self.audio_buffer.append(indata.copy())

    def stop_audio_capture(self):
        """
        音声取得の停止する。
        """
        if not self.is_recording:
            print("音声は取得していません。")
            return

        self.is_recording = False
        if self._thread is not None:
            self._thread.join()
            self._thread = None

        print("音声取得を終了しました。")
        # 録音データを保存
        data = self.get_recorded_data()
        print (data)
    
    def get_recorded_data(self) -> np.ndarray:
        """
        取得データを取得する。

        Returns:
            np.ndarray: 録音データ（NumPy配列形式）。
        """
        if not self.audio_buffer:
            print("録音データが存在しません。")
            return None
        return np.concatenate(self.audio_buffer)