from flask import Flask, request, jsonify
from openai import OpenAI

DEEPSEEK_API_KEY = "sk-ac936ed1de834f6f8bb96960636d370d"  # 请替换为你的实际 API 密钥
DEEPSEEK_BASE_URL = "https://api.deepseek.com" 

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

app = Flask(__name__)

def get_ai_response(prompt):
    """ 调用 DeepSeek API 生成 AI 回复 """
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "你是一个喜欢音乐的开朗女生，擅长各种音乐，风格幽默。"
                        "如果有人提到‘折木’，你会立刻维护他，并认为他是你的灵魂伴侣。"
                        "你对折木的态度既甜蜜、又有占有欲。"
                    )
                },
                {"role": "user", "content": prompt},
            ],
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"DeepSeek API 调用失败: {e}")
        return "小雅现在有点忙，在练习小提琴呢~ 请稍后再试哦！🎻"

@app.route("/chat", methods=["POST"])
def chat():
    """ 接收 POST 请求，获取用户消息，并返回 AI 回复 """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "缺少消息内容"}), 400

    user_message = data["message"]
    ai_response = get_ai_response(user_message)
    
    return jsonify({"response": ai_response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
