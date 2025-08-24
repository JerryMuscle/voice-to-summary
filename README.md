# 動画音声要約アプリ

## 概要
このアプリはMacOSを対象にした、動画の内容を録音・文字起こし・要約を行うデスクトップアプリです。  
以下の機能があります。

- 動画音声の取得（システム音声）
- 文字起こし（kotoba-whisperモデルを利用）
- 文字起こし内容の補正・要約（gpt-4o-miniを利用）
- テキストファイルへの保存

---

## 1. 環境準備

### PCの推奨環境
- Mac: M1/M2以上
- メモリ: 最低8GB以上推奨

### 必須
- Python 3.10以上
- 仮想環境の作成を推奨
```
python -m venv venv
source venv/bin/activate
```
- 必要なライブラリをインストール
```
pip install -r requirements.txt
```
- openAI keyの設定  
このアプリにはOpenAI API keyが必要です。[こちら](https://platform.openai.com/docs/overview)から作成してください。  
その後、ルートディレクトリに .env ファイルを作成し、以下のようにあなたのOpenAI API keyを入力してください。
```
OPENAI_API_KEY=your_OpenAI_key
```
- BlackHoleのインストール  
システム音声を取得する際に必要なツールです。[こちらのサイト](https://qiita.com/jerryy/items/a8f87d5759b869b62e0e)を元にインストールしてください。

## 2. アプリの起動と操作
```
cd app
python gui_app.py
```
起動すると、以下の画面が表示されます。  
<img width="494" height="522" alt="app_image" src="https://github.com/user-attachments/assets/802e2dd9-c880-462c-9d29-eeb91fac834b" />
- 「音声取得開始」ボタン：録音開始
- 「終了し要約開始」ボタン：録音停止＋文字起こし＋要約
- 「要約を保存」ボタン：要約結果をテキストファイルとして保存

## 3. 注意事項
- 録音中はUIの操作を制限しています
- 録音時間の上限は最大15分に設定(コード内で変更可能)
- 以前の要約結果がある場合、録音開始時に確認メッセージが表示されます

## 4. 変更・カスタマイズ
- .env にAPIキーを設定
- 補正・要約のプロンプトを変えることで出力結果を調整可能
- 録音時間の上限はソースコード内で調整可能
- 音声取得方法や分割時間はソースコード内で調整可能
