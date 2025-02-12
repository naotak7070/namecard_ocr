from logic.GPTFunction import GPTPropertyOutput

def main():
    gpt = GPTPropertyOutput()
    prompt = "リンゴは英語で何と呼ぶか6文字以内で回答して下さい"
    message, prompt_token,completion_token,model_name= gpt.chat(prompt)
    message = message.lower()  # 小文字に変換して検索しやすくする
    total_cost=gpt.calculateCostJPY(prompt_token,completion_token)
    
    print(message)
    print(total_cost)


if __name__ == "__main__":
    main()

