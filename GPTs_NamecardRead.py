import streamlit as st
import os
import tempfile
from PIL import Image
from logic.GPTFunction import GPTPropertyOutput
from logic.NamecardImageProcessFunction import ImageProcessorNamecard
from logic.NamecardReadPostProcessFunction import NamecardReadPostProcessor
import json

def main():
    st.title("名刺情報読み取りアプリ")
    
    # ユーザーに画像ファイルのアップロードを促す
    uploaded_file = st.file_uploader("名刺の写真をアップロードしてください", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        # 画像をPILで読み込み
        try:
            image = Image.open(uploaded_file)
        except Exception as e:
            st.error(f"画像の読み込みに失敗しました: {e}")
            return
        
        st.image(image, caption="アップロード画像", use_column_width=True)
        
        # ImageProcessorNamecard を利用して画像を縮小
        # resizeしてもコストはほとんど変わらないかもしれないので、この処理はいったん挟まない
        resize_factor=1.0
        processor = ImageProcessorNamecard()
        resized_image = processor.resize_image(image, resize_factor=resize_factor)
        
        # st.image(resized_image, caption=f"縮小後の画像 ({resize_factor})", use_column_width=True)
        
        # 一時ファイルに縮小画像を保存
        temp_dir = tempfile.gettempdir()
        temp_path = os.path.join(temp_dir, "temp_resized.jpg")
        try:
            resized_image.save(temp_path, format="JPEG")
        except Exception as e:
            st.error(f"一時ファイルへの保存に失敗しました: {e}")
            return
        
        # GPTPropertyOutput のインスタンスを生成し、readNamecard を実行
        gpt = GPTPropertyOutput()
        with st.spinner("名刺情報を読み取り中です..."):
            try:
                result, prompt_token, completion_token = gpt.readNamecard(temp_path)
            except Exception as e:
                st.error(f"名刺情報の読み取りに失敗しました: {e}")
                return
        
        # json抽出と変換
        post_processor=NamecardReadPostProcessor()
        json_content, error_msg = post_processor.json_extract(result)
        if error_msg:
            st.error(error_msg)
        else:
            try:
                data = post_processor.namecardJsonProcess(json_content)
                # pd_data=post_processor.namecardJsonToDataFrame(json_content)
            except Exception as e:
                st.error(f"JSONのパースに失敗しました: {e}")
   

        # 結果を表示
        st.write("### 読み取り結果")
        # st.write(result)
        st.write(data)
        # st.dataframe(pd_data)
        total_cost=gpt.calculateCostJPY(prompt_token,completion_token)
        st.write("**コスト(円):**", round(total_cost,4))
        st.write("**Prompt Tokens:**", prompt_token)
        st.write("**Completion Tokens:**", completion_token)
        
        

if __name__ == "__main__":
    main()
