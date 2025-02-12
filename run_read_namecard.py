import os
from os.path import join
from logic.GPTFunction import GPTPropertyOutput
from dotenv import load_dotenv

# .envファイルから環境変数をロードする場合は以下を有効にする
load_dotenv()

def main():
    # OpenAIのAPIキーが設定されているか確認
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable is not set.")
        return

    # サンプル画像のパスを指定（OSに合わせて適宜パス区切り文字を調整）
    image_path = join("sample", "meishi1_jpg.jpg")
    
    # GPTPropertyOutputのインスタンスを生成
    gpt = GPTPropertyOutput()

    try:
        # readNamecardを呼び出して、結果とトークン数を取得
        result, prompt_tokens, completion_tokens= gpt.readNamecard(image_path)
        print("=== API Response ===")
        print(result)
        print(f"Prompt Tokens: {prompt_tokens}")
        print(f"Completion Tokens: {completion_tokens}")

    except Exception as e:
        print("An error occurred while reading the namecard:")
        print(e)

if __name__ == "__main__":
    main()
    
