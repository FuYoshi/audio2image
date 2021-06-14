"""
The 'webapp' folder is connected to a github account (Yoshi) in order to deploy
the app using heroku.

Changes have to be pushed to github with:

$ git push origin master

and then the changes can be pushed to heroku with:

$ git push heroku master.

the webapplication can be found with:
https://multimedia-webapp.herokuapp.com/

myapp.py: this file contains the objects for the web application. Most of the
interactable objects of the web application are imported from streamlit. The
documentation of the streamlit API can be found here:
https://raw.githubusercontent.com/omnidan/node-emoji/master/lib/emoji.json

Procfile: this file is called by heroku to launch the web application.
requirements.txt: this file is used by heroku to import modules.
setup.sh: this file is used by heroku.
"""

import streamlit as st

st.title("WEB APP TITLE")


def image_to_audio(uploaded_file):
    """ Convert the uploaded image file to an audio file. """
    # TODO: convert image to audio instead of displaying it
    st.image(uploaded_file)


def audio_to_image(uploaded_file):
    """ Convert the uploaded audio file to an image file. """
    # TODO: convert audio to image instead of playing it
    st.audio(uploaded_file)


# Show the radio button widget to select the conversion mode.
mode = st.radio("Mode", ("image to audio", "audio to image"))

if mode == "image to audio":
    # Show the upload file widget that accepts image files.
    uploaded_file = st.file_uploader("Choose a file to convert",
        type=["png", "jpg", "jpeg"])

    # Convert the file after pressing the "convert" button.
    if uploaded_file is not None and st.button("Convert", key="image"):
        image_to_audio(uploaded_file)

elif mode == "audio to image":
    # Show the upload file widget that accepts sound files.
    uploaded_file = st.file_uploader("Choose a file to convert",
        type=["wav", "mp3"])

    # Convert the file after pressing the "convert" button.
    if uploaded_file is not None and st.button("Convert", key="audio"):
        audio_to_image(uploaded_file)


if st.button("Record"):
    # TODO: a way to record the user and convert it.
    st.write("recording...")
