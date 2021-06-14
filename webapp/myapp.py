import streamlit as st

st.title("WEB APP TITLE")


def image_to_audio(uploaded_file):
    # TODO: convert image to audio instead of displaying it
    st.image(uploaded_file)


def audio_to_image(uploaded_file):
    # TODO: convert audio to image instead of playing it
    st.audio(uploaded_file)


mode = st.radio("Mode", ("image to audio", "audio to image"))
if mode == "image to audio":
    uploaded_file = st.file_uploader("Choose a file to convert",
        type=["png", "jpg", "jpeg"])
    if uploaded_file is not None and st.button("Convert", key="image"):
        image_to_audio(uploaded_file)

elif mode == "audio to image":
    uploaded_file = st.file_uploader("Choose a file to convert",
        type=["wav", "mp3"])
    if uploaded_file is not None and st.button("Convert", key="audio"):
        audio_to_image(uploaded_file)


if st.button("Record"):

    # TODO
    st.write("recording...")
