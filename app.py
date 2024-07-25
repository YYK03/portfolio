import streamlit as st
# import openai 이문구는 이제 안 사용함
from openai import OpenAI

client = OpenAI(
    api_key = st.secrets["api_key"])
# api를 노출시킨 채 공개하면 요금 폭탄맞음. 절대하면 안되는 행위

st.title("GPT와 DALL-E를 이용해서 그림을 그려드립니다")

with st.form("form"):
    user_input = st.text_input("영어로 입력하세요. 특정인물(예: 있지 류진, 트와이스 사나, 라이즈 원빈 등)은 못그려냅니다..")
    size = st.selectbox("크기", ["1024x1024", "512x512", "256x256"])
    submit = st.form_submit_button("제출")

if submit and user_input: # 유저가 제출버튼을 눌렀을 떄, 내용이 있을 때 실행
    gpt_prompt = [{
        "role": "system",
        "content": "Imagine the detail appeareance of the input. Response it shortly."
    }]
    gpt_prompt.append({
        "role": "user",
        "content": user_input
    })
    with st.spinner("Waiting for ChatGPT..."):
        gpt_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=gpt_prompt
        )

    prompt = gpt_response.choices[0].message.content #구문이 업그레이드됨
    st.write(prompt)

    with st.spinner("Waiting for DALL-E..."):
        dalle_response = client.images.generate(
            prompt=prompt,
            size = size
    )

    st.image(dalle_response.data[0].url)

