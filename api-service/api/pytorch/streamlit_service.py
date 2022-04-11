from model import load_processor_model
from model import get_prediction
import streamlit as st
from PIL import Image
import asyncio


def load_image(image_file):
    img = Image.open(image_file)
    print("loading", type(img))
    return img


def file_selector():
    image_file = st.file_uploader("Upload Images", type=["png", "jpg", "jpeg"])

    if image_file is not None:
        # To View Uploaded Image
        st.image(load_image(image_file), width=250)
        return image_file


def read_data():
    image_file = file_selector()
    question = st.text_input('', 'Input your question here')
    return image_file, question


def predict(file, question):
    print("question is ", question)
    print("predict file:", file.size, type(file))

    # Make prediction
    prediction_results = {}
    answer = get_prediction(file, question)
    prediction_results['prediction_label_vilt'] = answer

    return prediction_results


if __name__ == "__main__":
    st.header("VigNet")
    st.subheader("This application will help you understand the things around you just by clicking a picture\
      of your surrounding and asking a question related to the picture. Please click on capture an image button\
      and click on the microphone to ask your question. You will get an answer within seconds!")
    st.write("")
    st.write("")
    asyncio.run(load_processor_model())
    image_file, question = read_data()
    if st.button('Ask'):
        answer = predict(image_file, question)['prediction_label_vilt']
        st.write(answer)
