import tkinter as tk
from services.recorder import Recorder
from services.transcribe import AudioTranscriber

class AudioSummaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title('動画音声要約アプリ')
        self.root.geometry('500x500')
        self.recorder = Recorder()
        self.transcriber = AudioTranscriber()
        self.create_widgets()

    def create_widgets(self):
        # 文字起こし
        self.summary_label = tk.Label(self.root, text="要約結果", font=("Arial", 14))
        self.summary_label.pack(pady=10)
        self.summary_text = tk.Text(self.root, height=25, width=50)
        self.summary_text.pack()

        # # 要約結果
        # self.summary_label = tk.Label(self.root, text="要約結果", font=("Arial", 14))
        # self.summary_label.pack(pady=10)
        # self.summary_text = tk.Text(self.root, height=25, width=50)
        # self.summary_text.pack()

        # 録音開始ボタン
        self.start_btn = tk.Button(
            self.root, text="音声取得開始", command=self.start_recording, 
            height=5, width=10)
        self.start_btn.place(x=50, y=400)

        # 録音終了ボタン
        self.stop_btn = tk.Button(
            self.root, text="終了し要約開始", command=self.stop_and_transcribe,
                height=5, width=10)
        self.stop_btn.place(x=350, y=400)

    def start_recording(self):
        """
        録音を開始する。
        """
        self.recorder.start_audio_capture()

    def stop_and_transcribe(self):
        """
        録音を停止して文字起こしを実行する。
        """
        self.recorder.stop_audio_capture()
        audio_data = self.recorder.get_recorded_data()

        if audio_data is not None:
            text = self.transcriber.transcribe_from_array(audio_data, self.recorder.sample_rate)
            self.summary_text.delete("1.0", tk.END)
            self.summary_text.insert(tk.END, text)
        else:
            self.summary_text.delete("1.0", tk.END)
            self.summary_text.insert(tk.END, "録音データがありません。")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSummaryApp(root)
    root.mainloop()