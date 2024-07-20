import streamlit as st
from PIL import Image
from src.services.aesthetic_predictor import predict

st.header("3Sides Image Aesthetics Scorer")


uploaded_files = st.file_uploader(
    "Choose images...", type=["png", "jpg", "jpeg"], accept_multiple_files=True
)

if uploaded_files:
    st.subheader("Input", divider="rainbow")
    images_and_scores = []

    for uploaded_file in uploaded_files:
        image = Image.open(uploaded_file)
        score = predict(image)
        images_and_scores.append((image, score, uploaded_file.name))

    images_and_scores.sort(key=lambda x: x[1], reverse=True)

    cols = st.columns(len(images_and_scores))

    for col, (image, score, filename) in zip(cols, images_and_scores):
        with col:
            st.image(image, caption=f"{filename} - Score: {score}", width=100)
else:
    st.warning("No images uploaded. Please upload images.")
