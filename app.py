from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os

from PIL import Image
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model=genai.GenerativeModel("gemini-pro-vision")

def get_gemini_response(input,image,user_prompt):
    response=model.generate_content([input,image[0],user_prompt])
    return response.text

def input_image_details(uploded_file):
    if uploded_file is not None:
        #read the file into bytes
        bytes_data=uploded_file.getvalue()

        image_parts=[
            {
                "mime_type":uploded_file.type,# Get the mime type of the uploaded file
                "data":bytes_data
            }
        ]

        return image_parts
    else:
        raise FileNotFoundError("No file uploded")

#streamlit

st.set_page_config(page_title="MultiLanguage Info Extractor")

st.header("MultiLanguage Info Extractor")

uploaded_file = st.file_uploader("Choose an image ...", type=["jpg", "jpeg", "png"])


if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.", use_column_width=True)

input=st.text_input("Ask me anything: ",key="input")
submit=st.button("Submit")

input_prompt="""
You are an expert in understanding invoices. We will upload a a image as invoice
and you will have to answer any questions based on the uploaded invoice image
"""

## if submit button is clicked

if submit:
    image_data=input_image_details(uploaded_file)
    response=get_gemini_response(input_prompt,image_data,input)
    st.subheader("The Response is")
    st.write(response)
