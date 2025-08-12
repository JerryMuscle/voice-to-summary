import sounddevice as sd
import numpy as np
import threading
import time

class Recorder:
    def __init__(self):

            self.sample_rate = 16000
            self.channels = 1
            self.is_recording = False
            self.audio_buffer = []
            self._thread = None
            self._on_stop = None

    def start_audio_capture(self, max_duration_sec=None, on_stop=None):
        """
        システム音声の音声取得を開始する。

        Args:
            max_duration_sec: 自動で終了する時間
            on_stop: コールバック用の変数
        """
        if self.is_recording:
            print("既に音声取得中です。")
            return

        self._on_stop = on_stop
        self.is_recording = True
        self.audio_buffer = []
        print("音声取得を開始しました...")

        def record():
            try:
                start_time = time.time()
                # BlackHoleを指定した入力ストリームを開く
                with sd.InputStream(samplerate=self.sample_rate, channels=self.channels, dtype='float32',
                                    device="BlackHole 2ch", callback=self.audio_callback):
                    while self.is_recording:
                        sd.sleep(100)
                        elapsed = time.time() - start_time
                        if elapsed >= max_duration_sec:
                            print("録音時間の上限に達したため、自動停止して要約を実行します。")
                            if self._on_stop:
                                self._on_stop()
                            break
            except Exception as e:
                print(f"録音スレッド中にエラー: {e}")
                self.safe_stop()

        # 録音スレッドを開始
        self._thread = threading.Thread(target=record, daemon=True)
        self._thread.start()

    def audio_callback(self, indata, frames, time, status):
        """
        音声データを録音バッファに追加するコールバック関数。

        Args:
            indata (np.ndarray): 取得した音声データ。
            frames (int): フレーム数。
            time (CData): 時間情報。
            status (CallbackFlags): ステータス情報。
        """
        if status:
            print(f"録音中にエラーが発生しました: {status}")
            return None
        self.audio_buffer.append(indata.copy())

    def stop_audio_capture(self):
        """
        音声取得を停止する。
        """
        if not self.is_recording:
            print("音声は取得していません。")
            return

        self.is_recording = False
        current_thread = threading.current_thread()
        if self._thread is not None and self._thread != current_thread:
            self._thread.join()
            
        self._thread = None
        print("音声取得を終了しました。")
    
    def get_recorded_data(self) -> np.ndarray:
        """
        音声データを取得する。

        Returns:
            np.ndarray: 録音データ（NumPy配列形式）。
        """
        if not self.audio_buffer:
            print("録音データが存在しません。")
            return None
        try:
            print("録音データを取得しています")
            return np.concatenate(self.audio_buffer)
        except Exception as e:
            print(f"録音データの結合に失敗しました: {e}")
            return None
    
    def safe_stop(self):
        """
        録音を安全に停止し、スレッドを終了する（例外・強制終了時用）
        """
        try:
            if self.is_recording:
                print("録音を強制停止します...")
                self.is_recording = False
            if self._thread is not None and self._thread.is_alive():
                if threading.current_thread() != self._thread:
                    self._thread.join(timeout=5)  # 強制終了の待機
                self._thread = None
            print("録音は安全に停止されました。")
        except Exception as e:
            print(f"録音停止中にエラーが発生しました: {e}")

    def clear_audio_buffer(self):
        """
            音声バッファをクリアする
             要約後にもう一度要約ボタンを押すと、処理が実施してしまうため
        """
        self.audio_buffer = []