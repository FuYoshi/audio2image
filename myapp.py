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
import rANDp
import os
import base64
from datetime import datetime


st.title("Audio to Image compression")
st.text("You can't hear images, or can you?")


def save_uploaded_file(uploaded_file):
    """ Save the uploaded file in the heroku directory. """
    # Code inspired by: https://blog.jcharistech.com/2021/01/21/how-to-save-uploaded-files-to-directory-in-streamlit-apps/
    with open(os.path.join("tempDir", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())


def download_link(filename):
    """ Return a link that downloads the given file.  """
    file = open(filename, 'rb')
    contents = file.read()
    data_url = base64.b64encode(contents).decode()
    date = datetime.now().strftime("%Y-%m-%d_%X")
    new_filename = "webapp_{}.png".format(date)
    href = f'<a href="data:file/png;base64,{data_url}" download="{new_filename}">Download</a>'
    return href


# Show the radio button widget to select the conversion mode.
mode_ati = "Audio to Image"
mode_ita = "Image to Audio"
mode = st.radio("Mode", (mode_ati, mode_ita))
if mode == mode_ati:
    # Show the upload file widgets.
    audio_file = st.file_uploader("Choose an audio file to convert",
                                  type=["wav"])

    # Convert the file after pressing the "convert" button.
    if audio_file is not None and st.button("Convert"):
        save_uploaded_file(audio_file)
        rANDp.record('test', 3)
        #result = converter.file_merge('./tempDir/' + image_file.name,
        #                              './tempDir/' + audio_file.name)
        #st.image(result.name)
        #st.markdown(download_link(result.name), unsafe_allow_html=True)

elif mode == mode_ita:
    # Show the upload file widget that accepts image files.
    image_file = st.file_uploader("Choose a image file to convert",
                                  type=["png"])

    # Convert the file after pressing the "convert" button.
    if image_file is not None and st.button("Convert"):
        save_uploaded_file(image_file)
        #im, a = converter.file_extract('./tempDir/' + image_file.name)
        #st.image(im.name)
        #st.audio(a.name)


if st.button("Record"):
    # TODO: a way to record the user and convert it.
    st.write("recording...")
