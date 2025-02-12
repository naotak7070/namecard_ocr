from logic.GPTFunction import GPTPropertyOutput
import os
import requests
import pytest
import base64
from os.path import join

def test_calculateCostJPY():
    gpt=GPTPropertyOutput()
    prompt_token=200
    completion_token=200
    result=gpt.calculateCostJPY(prompt_token,completion_token)

    assert result==(0.0775+0.3100),f"Expected {(0.0775+0.3100)} but got {result}" 


def test_chat(monkeypatch):
    # ダミーのレスポンスオブジェクトを作成
    def dummy_create(model, messages):
        # ダミーのメッセージオブジェクト
        DummyMessage = type("DummyMessage", (), {})()
        DummyMessage.content = "apple"
        
        # ダミーの選択肢オブジェクト
        DummyChoice = type("DummyChoice", (), {})()
        DummyChoice.message = DummyMessage
        
        # ダミーの使用量オブジェクト
        DummyUsage = type("DummyUsage", (), {})()
        DummyUsage.prompt_tokens = 10
        DummyUsage.completion_tokens = 20
        
        # ダミーのcompletionオブジェクト
        DummyCompletion = type("DummyCompletion", (), {})()
        DummyCompletion.choices = [DummyChoice]
        DummyCompletion.usage = DummyUsage
        DummyCompletion.model = model
        
        return DummyCompletion

    # ダミーの chat.completions を持つオブジェクト
    class DummyChatCompletions:
        def create(self, model, messages):
            return dummy_create(model, messages)

    class DummyChat:
        completions = DummyChatCompletions()

    # ダミーの OpenAI クラス
    class DummyOpenAI:
        def __init__(self, api_key):
            self.api_key = api_key
            self.chat = DummyChat()

    # テスト実行時に、logic.GPTFunction 内の OpenAI を DummyOpenAI に差し替える
    def test_chat(monkeypatch):
        # Monkeypatchにより、GPTFunction内の OpenAI クラスを DummyOpenAI に置き換える
        monkeypatch.setattr("logic.GPTFunction.OpenAI", DummyOpenAI)

        # 環境変数にダミーの API キーを設定（実際の通信は行われません）
        os.environ['OPENAI_API_KEY'] = 'dummy_api_key'
        
        # GPTPropertyOutput のインスタンスを生成し、chat を実行
        gpt = GPTPropertyOutput()
        prompt = "リンゴは英語で何と呼ぶか6文字以内で回答して下さい"
        message, prompt_tokens, completion_tokens, model_name = gpt.chat(prompt)
        
        # ダミーのレスポンス値と一致することを確認
        assert message == "apple", f"Expected message 'apple' but got {message}"
        assert prompt_tokens == 10, f"Expected prompt_tokens 10 but got {prompt_tokens}"
        assert completion_tokens == 20, f"Expected completion_tokens 20 but got {completion_tokens}"
        assert model_name == "gpt-4o", f"Expected model_name 'gpt-4o' but got {model_name}"

def test_readNamecard(monkeypatch):
    # 環境変数にダミーの API キーを設定
    os.environ['OPENAI_API_KEY'] = 'dummy_api_key'
    
    # テスト用の画像パス（サンプル画像が存在する必要があります）
    image_path = join("sample", "meishi1_jpg.jpg")
    
    # ダミーのレスポンス JSON
    dummy_response_json = {
        "usage": {
            "prompt_tokens": 123,
            "completion_tokens": 456
        },
        "choices": [
            {
                "message": {
                    "content": "Dummy response message"
                }
            }
        ],
        "model": "gpt-4o"
    }
    
    # ダミーのレスポンスオブジェクト
    class DummyResponse:
        def __init__(self, json_data, status_code=200):
            self._json_data = json_data
            self.status_code = status_code
        
        def raise_for_status(self):
            if not (200 <= self.status_code < 300):
                raise requests.HTTPError(f"Status code: {self.status_code}")
        
        def json(self):
            return self._json_data
    
    # requests.post をダミー関数に置き換える
    def dummy_post(url, headers, json):
        return DummyResponse(dummy_response_json, 200)
    
    monkeypatch.setattr(requests, "post", dummy_post)
    
    # GPTPropertyOutput のインスタンスを生成
    gpt = GPTPropertyOutput()
    
    # readNamecard メソッドを呼び出す
    result, prompt_token, completion_token = gpt.readNamecard(image_path)
    
    # 結果の検証
    assert result == dummy_response_json, "Response JSON does not match dummy data."
    assert prompt_token == dummy_response_json["usage"]["prompt_tokens"], "Prompt tokens do not match."
    assert completion_token == dummy_response_json["usage"]["completion_tokens"], "Completion tokens do not match."