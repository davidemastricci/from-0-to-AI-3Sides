import streamlit as st
from PIL import Image
from src.services.aesthetic_predictor import predict


st.header("3Sides Image Aesthetics Scorer")

uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])
picture_width = st.sidebar.slider("Picture Width", min_value=100, max_value=500)
if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.subheader("Input", divider="rainbow")
    st.image(image, caption="Uploaded Image", width=picture_width)
    results = predict(image)
    st.subheader("Results", divider="rainbow")
    st.image(image, caption=results, width=picture_width)
