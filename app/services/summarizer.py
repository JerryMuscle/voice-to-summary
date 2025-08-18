from openai import OpenAI, OpenAIError, APIConnectionError, RateLimitError
import os
from dotenv import load_dotenv
import traceback

class Summarizer:
    def __init__(self):
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        self.client = OpenAI(api_key = api_key)

    def correct_medical_terms(self, text) -> str:
        """
        OpenAI(gpt-4o-mini):医学用語、文の補正

        Args:
            text (str): 文字起こしした長文テキスト

        Returns:
            str: 補正されたテキスト
        
        """
        try:

            # プロンプト作成（補正指示）
            messages = [
                {"role": "system", "content": "あなたは医学の専門家です。"},
                {"role": "user", "content": f"""以下の文章は音声認識の結果です。
                    この文章を、医学的に正しい用語・表現に補正してください。できるだけ原文の意味や文脈は変えず、誤認識された用語を修正してください。
                    音声認識結果：「{text}」"""}
            ]

            response = self.client.responses.create(
                model="gpt-4o-mini",
                input=messages,
                store=True,
            )
            return response.output_text
        except APIConnectionError:
            return "APIサーバーへの接続に失敗しました。ネットワークを確認してください。"
        except RateLimitError:
            return "APIのリクエスト制限を超えました。しばらく待ってから再実行してください。"
        except OpenAIError as e:
            print("OpenAI APIエラー:", e)
            traceback.print_exc()
            return f"OpenAI APIでエラーが発生しました: {e}"
        except Exception as e:
            print("予期しないエラー:", e)
            traceback.print_exc()
            return f"予期しないエラーが発生しました: {e}"

        

    def summarize_text(self, text) -> str:
        """
        OpenAI(gpt-4o-mini): 内容の要約

        Args:
            text (str): 文字起こし(補正済)した長文テキスト

        Returns:
            str: 要約されたテキスト
        """

        try:

            # プロンプト作成（要約指示）
            messages = [
                {"role": "system", "content": "あなたは医学の専門家であり、優秀な日本語の文章要約者です。"},
                {"role": "user", "content": f"""以下は医学的な内容の会話やプレゼンの文字起こしです。内容を要約してください。
                    ・重要な点を箇条書きで整理してください。
                    ・話の流れがわかるよう、段落ごとに適切に改行してください。
                    【文字起こし】:{text}"""}
            ]

            response = self.client.responses.create(
                model="gpt-4o-mini",
                input=messages,
                store=True,
            )
            return response.output_text
        except APIConnectionError:
            return "APIサーバーへの接続に失敗しました。ネットワークを確認してください。"
        except RateLimitError:
            return "APIのリクエスト制限を超えました。しばらく待ってから再実行してください。"
        except OpenAIError as e:
            print("OpenAI APIエラー:", e)
            traceback.print_exc()
            return f"OpenAI APIでエラーが発生しました: {e}"
        except Exception as e:
            print("予期しないエラー:", e)
            traceback.print_exc()
            return f"予期しないエラーが発生しました: {e}"
