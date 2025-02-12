import streamlit as st
from logic.GPTFunction import GPTPropertyOutput

st.title('GPTs Test')
st.write('これはGPTの接続テストです。ただのchatGPTです。')

# GPTPropertyOutput のインスタンスを生成
gpt = GPTPropertyOutput()

# ユーザーにプロンプトを入力してもらう
prompt = st.text_input("Enter your prompt:")

# ボタンを押したら処理を実行
if st.button("Send"):
    if prompt.strip():
        # chat メソッドを呼び出し、結果を受け取る
        message, prompt_token,completion_token,model_name = gpt.chat(prompt)
        
        st.markdown("### Response")
        st.write(message)
        
        st.markdown("### Token Usage, Costs")
        st.write("Model name: ", model_name)
        st.write("Prompt tokens: ", prompt_token)
        st.write("Completion tokens: ", completion_token)
        total_cost=gpt.calculateCostJPY(prompt_token,completion_token)

        st.write("Total Cost(JPY): ", total_cost)


    else:
        st.error("Please enter a prompt.")