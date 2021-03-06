#

import streamlit as st
import rec
import isc
import os
import base64
from datetime import datetime

# Title and information for the app and the user.
st.title("Audio to Image compression")
st.text("You can't hear images, or can you? \n"
        + "Made by: Coen de Graaf, Yoshi Fu & Lennaert Feijtes")
# Markdown
st.markdown("#### What is this?")
st.text("This application is part of our Multimedia project and lets the user expierence our"
+ "\nimplemented functionality.")

st.markdown("#### What does it do?")
st.text("Our program lets the user compress and encrypt audio files. This is achieved \n"
        + "by turning the audio-file into a .png file and by making use of a\n"
        + "randomely generated 16 bit salt based on an user given password.")

st.markdown("#### How does it work?")
st.markdown("##### Audio to image:")
st.text("1. Record a sound and download it.\n"
        + "2. Upload the recording and give a password. Press convert when ready. \n"
        + "3. Download the image.")

st.markdown("##### Image to Audio:")
st.text("1. Upload an image. Make sure this is an image generated by our program!\n"
        + "2. Enter the password you gave the image.\n"
        + "3. Convert the image and listen to the sound. You may also download it.")

st.markdown("# Try it yourself!")

# Saves uploaded file in the tempDir directory.
def save_uploaded_file(uploaded_file):
    """ Save the uploaded file in the heroku directory. """
    # Code inspired by: https://blog.jcharistech.com/2021/01/21/how-to-save-uploaded-files-to-directory-in-streamlit-apps/
    with open(os.path.join("tempDir", uploaded_file.name), "wb") as f:
        f.write(uploaded_file.getbuffer())

# Generates a download link for the user.
def download_link(filename):
    """ Return a link that downloads the given file.  """
    file = open(filename, 'rb')
    contents = file.read()
    data_url = base64.b64encode(contents).decode()
    date = datetime.now().strftime("%Y-%m-%d_%X")
    new_filename = "webapp_{}.png".format(date)
    href = f'<a href="data:file/png;base64,{data_url}" download="{new_filename}">Download</a>'
    return href


# Show the radio button widget to select the mode.
mode_ati = "Audio to Image"
mode_ita = "Image to Audio"
mode_rec = "Record a sound"
mode = st.radio("Select your option", (mode_rec, mode_ati, mode_ita, ))

if mode == mode_ati:
    # Show the upload .wav widgets.
    image_file = st.file_uploader("Choose an image file to convert",
                                  type=["wav"])
    psw = st.text_input("Enter password for encryption:", "", 20)

    # Convert the file after pressing the "convert" button, only if
    # image and password have been supplied.
    if image_file is not None and psw != "" and st.button("Convert to image!"):
        save_uploaded_file(image_file)
        isc.wav_to_image('./tempDir/' + image_file.name, 'ti', psw)
        result = 'ti.png'

        st.text("Click ???? to download the generated image!")
        st.markdown(download_link(result), unsafe_allow_html=True)
        os.remove('ti.png')
elif mode == mode_rec:

    # User input for amount of seconds of recording. For this app, people can
    # record from 3 to 10 seconds.
    seconds = st.number_input("How long do you want to record? (in seconds)", 3, 10, 3)

    # Exectues record function.
    if st.button("Record a sound!"):
        st.text("*** RECORDING ***")
        rec.record('temp69', int(seconds))
        audio_file = 'temp69.wav'
        st.text("*** DONE ***")
        st.audio(audio_file)
        os.remove('temp69.wav')

elif mode == mode_ita:

    # Show the upload file widget that accepts image files.
    image_file = st.file_uploader("Choose an image file to convert",
                                  type=["png"])
    pswDec = st.text_input("Enter password for decryption:", "", 20)

    # Convert the file after pressing the "convert" button, only if
    # image and password have been given by the user
    if image_file is not None and pswDec != "" and st.button("Convert to sound!"):
        save_uploaded_file(image_file)
        # Catches possible password fault.
        try:
                isc.image_to_wav('./tempDir/' + image_file.name, 'ts', pswDec, "wav")
                a = 'ts.wav'
                st.audio(a)
                os.remove('ts.wav')
        except:
                st.text("Password invalid!")
