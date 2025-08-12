import tkinter as tk
from tkinter import filedialog, messagebox
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
        # ステータス表示用ラベル
        self.status_label = tk.Label(self.root, text="ステータス: 待機中", fg="blue", font=("Arial", 10))
        self.status_label.pack(pady=5)

        # 要約結果表示
        self.summary_label = tk.Label(self.root, text="要約結果", font=("Arial", 14))
        self.summary_label.pack(pady=10)
        self.summary_text = tk.Text(self.root, height=25, width=50)
        self.summary_text.pack()

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

        # 保存ボタン
        self.save_button = tk.Button(root, text="要約を保存", command=self.save_summary_to_file)
        self.save_button.pack(pady=5)

    def set_status(self, text, busy=True):
        """
            ステータス表示とボタン制御をまとめて行う
        """
        self.status_label.config(text=f"ステータス: {text}")
        state = "disabled" if busy else "normal"
        self.start_btn.config(state=state)
        self.save_button.config(state=state)

    def start_recording(self):
        """
            録音を開始する。
                max_duration_secの時間分経過後、自動で録音停止⇨要約を実施
                とりあえず15分に設定
        """
        summary = self.summary_text.get("1.0", tk.END).strip()

        if summary:
            proceed = messagebox.askokcancel(
                "確認",
                "前回の要約結果があります。\n録音を開始すると上書きされますが、よろしいですか？"
            )
            if not proceed:
                return
        
        self.set_status("録音中...", busy=True)
        self.recorder.start_audio_capture(max_duration_sec=900, on_stop=self.stop_and_transcribe)

    def stop_and_transcribe(self):
        """
            録音を停止して文字起こし⇨内容の要約を実施する
        """
        print("文字起こしを開始します")
        self.set_status("要約中...", busy=True)
        self.recorder.stop_audio_capture()              # 録音の停止
        audio_data = self.recorder.get_recorded_data()  # 音声データの取得
        self.recorder.clear_audio_buffer()
        
        if audio_data is not None:
            # 文字起こしと要約の実施
            text = self.transcriber.transcribe_from_array(audio_data, self.recorder.sample_rate)
            self.summary_text.delete("1.0", tk.END)
            self.summary_text.insert(tk.END, text)
            self.set_status("待機中", busy=False) 
        else:
            self.set_status("待機中", busy=False) 
            messagebox.showwarning("警告", "録音データがありません")

    def save_summary_to_file(self):
        """
            テキストファイルへの出力
        """
        # テキストボックスの中身を取得
        summary = self.summary_text.get("1.0", tk.END).strip()

        if not summary:
            messagebox.showwarning("警告", "要約テキストが空です。")
            return

        # ファイルダイアログを開く
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")],
            title="要約の保存先を選択"
        )

        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(summary)
                messagebox.showinfo("完了", "要約を保存しました。")
            except Exception as e:
                messagebox.showerror("エラー", f"ファイルの保存に失敗しました:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioSummaryApp(root)
    root.mainloop()