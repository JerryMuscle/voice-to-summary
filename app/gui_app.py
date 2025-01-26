import tkinter as tk
from services.recorder import start_audio_capture, stop_audio_capture

class AudioSummaryApp:
    def __init__(self, root):
        self.root = root
        self.root.title('動画音声要約アプリ')
        self.root.geometry('500x500')
        self.create_widgets()

    def create_widgets(self):
        # 要約結果表示
        self.summary_label = tk.Label(self.root, text="要約結果", font=("Arial", 14))
        self.summary_label.pack(pady=10)
        self.summary_text = tk.Text(self.root, height=25, width=50)
        self.summary_text.pack()

        # 録音開始ボタン
        self.start_btn = tk.Button(self.root, text="Recording", command=start_audio_capture)
        self.start_btn.place(x=50, y=400)

        # 録音終了ボタン
        self.stop_btn = tk.Button(self.root, text="stop\n and\n sumarize", command=stop_audio_capture)
        self.stop_btn.place(x=350, y=400)

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSummaryApp(root)
    root.mainloop()