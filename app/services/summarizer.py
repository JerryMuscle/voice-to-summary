import torch
import soundfile as sf
from transformers import AutoFeatureExtractor, AutoModel

# モデルのロード（Base または Large）
model_name = "rinna/japanese-hubert-large"
feature_extractor = AutoFeatureExtractor.from_pretrained(model_name)
model = AutoModel.from_pretrained(model_name)
model.eval()

def summarize_text(temp_filename) -> str:
    """
    長文テキストを LongT5 を使用して要約する関数。

    Args:
        text (str): 文字起こしした長文テキスト

    Returns:
        str: 要約されたテキスト
    """

    raw_speech_16kHz, sr = sf.read(temp_filename)
    inputs = feature_extractor(
        raw_speech_16kHz,
        return_tensors="pt",
        sampling_rate=sr,
    )
    outputs = model(**inputs)
    # # 入力テキストをトークナイズ（LongT5 は最大 16K トークンを処理可能）
    # inputs = tokenizer(text, return_tensors="pt", max_length=16384, truncation=True)
    
    # # モデルが GPU なら入力も GPU に送る
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    # inputs = {k: v.to(device) for k, v in inputs.items()}

    # # 要約を生成
    # with torch.no_grad():
    #     summary_ids = model.generate(**inputs, max_length=200, min_length=50, length_penalty=2.0, num_beams=4)

    # # 要約結果をデコードして返す
    # summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return outputs