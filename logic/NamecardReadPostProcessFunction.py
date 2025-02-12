# NamecardReadPostProcessFunction.py
import re
import json
import uuid
import pandas as pd

class NamecardReadPostProcessor:
    def __init__(self):
        pass

    def json_extract(self, result):
        """
        result から JSON 部分を抽出し、抽出に成功した場合は (json_content, None) を、
        失敗した場合は (None, error_message) を返します。
        """
        if result is None:
            return None, "OCR結果が取得できませんでした。"

        if 'choices' not in result or len(result['choices']) == 0:
            return None, "LLMの応答が正しくありません。"

        extract = result['choices'][0]['message']['content']

        # content 内の JSON 部分を抽出
        match = re.search(r'```json\n(.*?)\n```', extract, re.DOTALL)
        if match:
            json_content = match.group(1)
            return json_content, None
        else:
            return None, "JSON形式のデータが見つかりませんでした。"
        
    def namecardJsonProcess(self,json_content):
        """
        JSON文字列を辞書に変換して返します。
        
        Parameters:
            json_content (str): JSON形式の文字列
            
        Returns:
            dict: 変換された辞書
        """
        data = json.loads(json_content)
        return data

    def namecardJsonToDataFrame(self,json_content):
        """
        JSON文字列を辞書に変換し、BusinessCardInformation部分を pandas DataFrame に変換して返します。
        
        Parameters:
            json_content (str): JSON形式の文字列
            
        Returns:
            pandas.DataFrame: BusinessCardInformation を含むデータフレーム
        """
        # JSON文字列を辞書に変換
        data = self.namecardJsonProcess(json_content)
        # "BusinessCardInformation" キーが存在するか確認
        info = data.get("BusinessCardInformation", {})
        
        # 辞書をDataFrameに変換（単一行のDataFrameとなる）
        df = pd.DataFrame([info])
        
        return df



        