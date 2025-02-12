import json
import pandas as pd
import pytest
from logic.NamecardReadPostProcessFunction import NamecardReadPostProcessor

def test_json_extract_success():
    """
    正しい形式のJSONブロックが含まれる場合、抽出されたJSON文字列が返されることを確認するテスト
    """
    processor = NamecardReadPostProcessor()
    sample_json = '{"BusinessCardInformation": {"CompanyName": "Test Inc.", "Email": "test@test.com"}}'
    sample_result = {
        "choices": [
            {
                "message": {
                    "content": f"```json\n{sample_json}\n```"
                }
            }
        ]
    }
    extracted, error = processor.json_extract(sample_result)
    assert error is None
    assert extracted == sample_json

def test_json_extract_none_result():
    """
    result が None の場合、エラーメッセージが返ることを確認するテスト
    """
    processor = NamecardReadPostProcessor()
    extracted, error = processor.json_extract(None)
    assert extracted is None
    assert error == "OCR結果が取得できませんでした。"

def test_json_extract_no_choices():
    """
    choices キーが存在しない場合、エラーメッセージが返ることを確認するテスト
    """
    processor = NamecardReadPostProcessor()
    sample_result = {}  # choicesキーがない
    extracted, error = processor.json_extract(sample_result)
    assert extracted is None
    assert error == "LLMの応答が正しくありません。"

def test_json_extract_no_json():
    """
    content 内にJSONブロックが見つからない場合、エラーメッセージが返ることを確認するテスト
    """
    processor = NamecardReadPostProcessor()
    sample_result = {
        "choices": [
            {
                "message": {
                    "content": "これはJSONブロックではないテキストです。"
                }
            }
        ]
    }
    extracted, error = processor.json_extract(sample_result)
    assert extracted is None
    assert error == "JSON形式のデータが見つかりませんでした。"

def test_namecardJsonProcess():
    """
    JSON文字列を辞書に変換できることを確認するテスト
    """
    processor = NamecardReadPostProcessor()
    sample_json = '{"BusinessCardInformation": {"CompanyName": "Test Inc.", "Email": "test@test.com"}}'
    data = processor.namecardJsonProcess(sample_json)
    assert isinstance(data, dict)
    assert "BusinessCardInformation" in data
    assert data["BusinessCardInformation"]["CompanyName"] == "Test Inc."
    assert data["BusinessCardInformation"]["Email"] == "test@test.com"

def test_namecardJsonToDataFrame():
    """
    JSON文字列から、BusinessCardInformation部分を含む pandas DataFrame が生成されることを確認するテスト
    """
    processor = NamecardReadPostProcessor()
    sample_json = '{"BusinessCardInformation": {"CompanyName": "Test Inc.", "Email": "test@test.com"}}'
    df = processor.namecardJsonToDataFrame(sample_json)
    # DataFrame で1行のデータが作成されるはず
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    # 辞書のキーが DataFrame のカラムとして存在するかをチェック
    assert "CompanyName" in df.columns
    assert "Email" in df.columns
    # 各カラムの値をチェック
    assert df.loc[0, "CompanyName"] == "Test Inc."
    assert df.loc[0, "Email"] == "test@test.com"
