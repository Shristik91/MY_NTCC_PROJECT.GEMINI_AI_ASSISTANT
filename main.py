import os
import json
import streamlit as st
from PIL import Image
from google import genai

# Load API key
working_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(working_dir, "config.json")

with open(config_path, "r") as file:
    config_data = json.load(file)

GOOGLE_API_KEY = config_data["GOOGLE_API_KEY"]
client = genai.Client(api_key=GOOGLE_API_KEY)

# Streamlit page
st.set_page_config(
    page_title="Gemini AI Assistant",
    page_icon="🤖"
)

st.title("🤖 Gemini AI Assistant")
st.write("Ask a question or upload an image.")

# User input
prompt = st.text_area(
    "Enter your question:",
    placeholder="Ask anything..."
)

uploaded_file = st.file_uploader(
    "Upload an image (optional)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded image", width=300)

if st.button("Generate Response"):
    if not prompt.strip():
        st.warning("Please enter a question.")
    else:
        try:
            with st.spinner("Gemini is thinking..."):

                contents = [prompt]

                if uploaded_file:
                    image = Image.open(uploaded_file)
                    contents.append(image)

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=contents
                )

            st.subheader("Gemini's Response")
            st.write(response.text or "No text response returned.")

        except Exception as e:
            st.error(f"Something went wrong: {e}")