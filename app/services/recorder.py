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
            self.channels = 1
            self.is_recording = False
            self.audio_buffer = []
            self._thread = None

    def start_audio_capture(self):
        """
        非同期での録音を開始
        録音データはメモリ上に保持される。
        """

        if self.is_recording:
            print("既に録音中です。")
            return

        self.is_recording = True
        self.audio_buffer = []  # 録音データを初期化

        def record():
            print("録音を開始しました...")
            with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, dtype='int16', callback=self.audio_callback):
                while self.is_recording:
                    sd.sleep(100)  # 100ms間隔でバッファを保持し続ける
            print("録音が終了しました。")

        # 録音を別スレッドで実行
        threading.Thread(target=record, daemon=True).start()

    def audio_callback(self, indata, frames, time, status):
        """
        音声データを録音バッファに追加するコールバック関数。

        Args:
            indata (np.ndarray): 録音されたデータ。
            frames (int): フレーム数。
            time (CData): 時間情報。
            status (CallbackFlags): ステータス情報。
        """
        if status:
            print(f"録音中にエラーが発生しました: {status}")
        self.audio_buffer.append(indata.copy())

    def stop_audio_capture():
        """
        録音の停止
        """