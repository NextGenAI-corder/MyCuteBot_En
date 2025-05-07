import os
from openai import OpenAI

def get_chatgpt(): #ChatGPTの応答を得る関数
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) #環境変数からAPIきーを取得

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "こんにちは！ゴールデンウィークはどこか行きましたか？何か日本で事故とかありましたか？"}],#プロンプト
        max_tokens=300
        # Limit the maximum number of tokens in the response (shorter replies)
    )

    print(response.choices[0].message.content)

if __name__ == "__main__":
    get_chatgpt()