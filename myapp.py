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
import converter
import os


st.title("WEB APP TITLE")


def save_uploaded_file(uploaded_file):
    """ Save the uploaded file in the heroku directory. """
    # Code inspired by: https://blog.jcharistech.com/2021/01/21/how-to-save-uploaded-files-to-directory-in-streamlit-apps/
    with open(os.path.join("tempDir", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())


# Show the radio button widget to select the conversion mode.
mode_merge = "merge"
mode_extract = "extract"
mode = st.radio("Mode", (mode_merge, mode_extract))
if mode == mode_merge:
    # Show the upload file widgets.
    image_file = st.file_uploader("Choose an image file",
                                  type=["png", "jpg", "jpeg"])
    audio_file = st.file_uploader("Choose an audio file",
                                  type=["wav", "mp3"])

    # Convert the file after pressing the "convert" button.
    if image_file and audio_file is not None and st.button("Merge"):
        save_uploaded_file(image_file)
        save_uploaded_file(audio_file)
        result = converter.file_merge('./tempDir/' + image_file.name,
                                      './tempDir/' + audio_file.name)
        st.image(result.name)

elif mode == mode_extract:
    # Show the upload file widget that accepts image files.
    image_file = st.file_uploader("Choose a file to convert",
                                  type=["png", "jpg", "jpeg"])

    # Convert the file after pressing the "convert" button.
    if image_file is not None and st.button("Extract"):
        save_uploaded_file(image_file)
        im, a = converter.file_extract('./tempDir/' + image_file.name)
        st.image(im.name)
        st.audio(a.name)


if st.button("Record"):
    # TODO: a way to record the user and convert it.
    st.write("recording...")
