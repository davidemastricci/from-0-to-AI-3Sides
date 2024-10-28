import streamlit as st
from PIL import Image
from src.services.aesthetic_predictor import predict

# Attempt to import process_image only if the OPENAI_API_KEY is present
try:
    from src.services.autocaption import process_image
    from src.common.utils import is_openai_key_valid  # Import the function
except ValueError as e:
    process_image = None


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

    if "results" not in st.session_state:
        st.session_state["results"] = {}
    cols = st.columns(len(images_and_scores))

    # Check if OPENAI_API_KEY is present and valid
    if process_image:
        if is_openai_key_valid():
            for col, (image, score, filename) in zip(cols, images_and_scores):
                with col:
                    st.image(image, caption=f"{filename} - Score: {score}", width=100)
                    if st.button(f"Process {filename}"):
                        with st.spinner(f"AI is generating content for {filename}..."):
                            result = process_image(image)
                            st.session_state.results[filename] = result

                    # Display the result if it exists in the session state
                    if filename in st.session_state.results:
                        st.write(f"{st.session_state.results[filename]}")
        else:
            st.warning(
                "OpenAI API key is not valid. Autocaptioning functionality is disabled."
            )
    else:
        st.warning("OpenAI API key is missing. Processing functionality is disabled.")
        for col, (image, score, filename) in zip(cols, images_and_scores):
            with col:
                st.image(image, caption=f"{filename} - Score: {score}", width=100)
                # Display the result if it exists in the session state
                if filename in st.session_state.results:
                    st.write(f"{st.session_state.results[filename]}")

else:
    st.warning("No images uploaded. Please upload images.")
