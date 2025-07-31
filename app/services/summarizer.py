from openai import OpenAI
import os
from dotenv import load_dotenv

def summarize_text(text) -> str:
    """
    あんまりいいモデルがなさそうだから、OpenAIのモデルにする

    Args:
        text (str): 文字起こしした長文テキスト

    Returns:
        str: 要約されたテキスト
    """

    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key = api_key)
    # プロンプト作成（要約指示）
    messages = [
        {"role": "system", "content": "あなたは医学の専門家であり、優秀な日本語の文章要約者です。"},
        {"role": "user", "content": f"""以下は医学的な内容の会話やプレゼンの文字起こしです。いくつか不自然な部分がありますが補完して、内容を要約してください。
            ・重要な点を箇条書きで整理してください。
            ・話の流れがわかるよう、段落ごとに適切に改行してください。
            【文字起こし】:{text}"""}
    ]

    response = client.responses.create(
        model="gpt-4o-mini",
        input=messages,
        store=True,
    )
    return response.output_text