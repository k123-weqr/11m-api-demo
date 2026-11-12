import sys
from openai import OpenAI
from dotenv import load_dotenv
import os

sys.stdout.reconfigure(encoding="utf-8")
load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)
def chat():
    messages = []
    print("===== DeepSeek 多轮对话，输入 exit 退出 =====")
    while True:
        user_input = input("\n你：")
        if user_input.strip().lower() == "exit":
            print("退出对话")
            break
        messages.append({"role": "user", "content": user_input})
        try:
            resp = client.chat.completions.create(
                model="deepseek-flash",
                messages=messages
            )
            reply = resp.choices[0].message.content
            print(f"模型：{reply}")
            messages.append({"role": "assistant", "content": reply})
        except Exception as e:
            print(f"出错啦：{e}")

if __name__ == "__main__":
    chat()