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
    
    # セッション状態にカメラ起動フラグを初期化
    if "camera_active" not in st.session_state:
        st.session_state.camera_active = False

    # 「カメラを起動する」ボタンを表示
    if st.button("カメラを起動する"):
        st.session_state.camera_active = True

    # カメラ起動フラグがTrueの場合、カメラ入力ウィジェットを表示
    if st.session_state.camera_active:
        uploaded_file = st.camera_input("名刺の写真を撮ってください")
        
        if uploaded_file is not None:
            # カメラ入力からの画像は BytesIO として渡されるので、PIL で開く
            try:
                image = Image.open(uploaded_file)
            except Exception as e:
                st.error(f"画像の読み込みに失敗しました: {e}")
                return
            
            st.image(image, caption="撮影画像")
            
            # ImageProcessorNamecard を利用して画像を縮小（ここでは縮小率は 1.0 で元画像を使用）
            resize_factor = 1.0
            processor = ImageProcessorNamecard()
            resized_image = processor.resize_image(image, resize_factor=resize_factor)
            
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
            
            # JSON抽出と変換
            post_processor = NamecardReadPostProcessor()
            json_content, error_msg = post_processor.json_extract(result)
            if error_msg:
                st.error(error_msg)
                return
            else:
                try:
                    data = post_processor.namecardJsonProcess(json_content)
                except Exception as e:
                    st.error(f"JSONのパースに失敗しました: {e}")
                    return

            # 結果を表示
            st.write("### 読み取り結果")
            st.write(data)
            total_cost = gpt.calculateCostJPY(prompt_token, completion_token)
            st.write("**コスト(円):**", round(total_cost, 4))
            st.write("**Prompt Tokens:**", prompt_token)
            st.write("**Completion Tokens:**", completion_token)

if __name__ == "__main__":
    main()
