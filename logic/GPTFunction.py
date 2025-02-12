from dotenv import load_dotenv
import os
from openai import OpenAI
import requests
import base64

# .env ファイルの内容を読み込む
load_dotenv()

class GPTPropertyOutput:
    def __init__(self):
        pass

    # コスト計算
    def calculateCostJPY(self,prompt_token,completion_token):
        # GPTs APIの料金モデル ($/1Mトークン)に合わせて日本円でのトータルコストを計算
        costUnit=1_000_000 #単価の分母（1M）
        USDJPYrate=155 #レート前提
        promptUnitpriceUSD=2.5 # プロンプト（input)コスト $/1M tokens
        completionUnitpriceUSD=10 # コンプレ-ション（output)コスト $/1M tokens
        input_costJPY=round((float(prompt_token)/ costUnit)* promptUnitpriceUSD*USDJPYrate,4)
        output_costJPY=round((float(completion_token)/ costUnit)* completionUnitpriceUSD*USDJPYrate,4)
        total_costJPY=input_costJPY+output_costJPY

        return total_costJPY

    # chatGPT（テスト用）
    def chat(self, prompt):
        api_key=os.getenv('OPENAI_API_KEY')
        self.client= OpenAI(api_key=api_key)
        completion = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "あなたは日本語で返答します"},
                {"role": "user", "content": prompt}
                ]
                )
        # result
        result=completion

        # 処理結果の取得
        message=completion.choices[0].message.content
        prompt_token=completion.usage.prompt_tokens
        completion_token=completion.usage.completion_tokens
        model_name=completion.model

        return message, prompt_token,completion_token,model_name
    

    # 画像ファイルをutf-8のテキストデータに変換
    def encode_image(self,imagepath):
            with open(imagepath, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')

    # 名刺イメージから
    def readNamecard(self,image_path):
        api_key = os.getenv('OPENAI_API_KEY')
        base64_image = self.encode_image(image_path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        payload = {
            "model": "gpt-4o",
            "messages": [
            {
                "role": "user",
                "content": [
                {
                    "type": "text",
                    "text":  """
                    ゴール
                    提供されたイメージには名刺情報あるいは企業情報が含まれており、そのイメージに含まれている
                    情報を以下の出力例に含まれている情報を抽出して出力すること
                    提供されたイメージに該当情報がない場合はNaNとして出力すること

                    出力例
                    {
                        "BusinessCardInformation": {
                            "CompanyName": "AAA農園",
                            "DepartmentName": "営業部",
                            "Position": "課長",
                            "FullName": "上岡龍太郎",
                            "TelephoneNumber": "0900-99-9998",
                            "MobilePhoneNumber": "090-1111-1111",
                            "Email": "aaa@korporation.com",
                            "PostalCode": "123-4567",
                            "Address": "愛知県名古屋市中区松原一丁目1番11号",
                            "URL":"https://www.test.com"
                        }
                    }

                    """
                },
                {
                    "type": "image_url",
                    "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
                ]
            }
            ],
        }

        # error handle
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            # HTTPステータスコードが200番台でない場合に例外を発生させる
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            raise Exception(f"HTTP error occurred: {http_err}")
        except Exception as err:
            raise Exception(f"Error during API request: {err}")

        try:
            result = response.json()
        except ValueError:
            raise Exception("Failed to parse JSON response from the API.")

        # レスポンスに必要なキーが含まれているか検証
        if 'usage' not in result:
            raise Exception("Invalid response: 'usage' field is missing.")
        if 'prompt_tokens' not in result['usage'] or 'completion_tokens' not in result['usage']:
            raise Exception("Invalid response: Token usage information is missing.")

        prompt_token = result['usage']['prompt_tokens']
        completion_token = result['usage']['completion_tokens']

        return result, prompt_token, completion_token


