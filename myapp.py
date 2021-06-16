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


st.title("WEB APP TITLE")


# Show the radio button widget to select the conversion mode.
mode_merge = "merge"
mode_extract = "extract"
mode = st.radio("Mode", (mode_merge, mode_extract))

if mode == mode_merge:
    # Show the upload file widgets.
    image = st.file_uploader("Choose an image file",
        type=["png", "jpg", "jpeg"])
    audio = st.file_uploader("Choose an audio file",
        type=["wav", "mp3"])

    # Convert the file after pressing the "convert" button.
    if image and audio is not None and st.button("Merge"):
        converter.file_merge('./' + image.name, './' + audio.name, None)

elif mode == mode_extract:
    # Show the upload file widget that accepts image files.
    uploaded_file = st.file_uploader("Choose a file to convert",
        type=["png", "jpg", "jpeg"])

    # Convert the file after pressing the "convert" button.
    if uploaded_file is not None and st.button("Extract"):
        converter.file_extract(uploaded_file.name, None)

if st.button("Record"):
    # TODO: a way to record the user and convert it.
    st.write("recording...")
