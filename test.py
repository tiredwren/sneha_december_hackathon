import streamlit as st
import pytz
import streamlit as st
import streamlit_authenticator as stauth
from deps import sign_up, fetch_users

import joblib
import numpy as np
import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime
from streamlit_option_menu import option_menu
from localStoragePy import localStoragePy
from deta import Deta
from streamlit_option_menu import option_menu
import streamlit as st
import numpy as np
import cv2
from tensorflow import keras
from keras.models import model_from_json
from keras.preprocessing.image import img_to_array
from streamlit_webrtc import VideoTransformerFactory, webrtc_streamer, VideoTransformerBase

import functions.home, functions.ai, functions.emo, functions.add 


def authenticate_user(username, users):
    """Authenticate the user."""
    credentials = {'usernames': {}}
    for user in users:
        credentials['usernames'][user['username']] = {'name': user['key'], 'password': user['password']}

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

    email, authentication_status, authenticated_username = Authenticator.login(':green[log in]', 'main')

    return authentication_status, authenticated_username


def login():
    if 'users' not in st.session_state:
        st.session_state.users = fetch_users()

    users = st.session_state.users
    emails = [user['key'] for user in users]
    usernames = [user['username'] for user in users]

    entered_username = st.text_input("Enter your username:")

    if st.button("Log In"):
        if entered_username in usernames:
            authentication_status, authenticated_username = authenticate_user(entered_username, users)

            if authentication_status:
                # User successfully authenticated
                st.sidebar.subheader(f'Hello {authenticated_username}!')
                # Continue with the rest of your app logic

            elif not authentication_status:
                st.error('Incorrect password for the username')
            else:
                st.warning('Please enter your credentials')

        else:
            # Username not found in the database, show sign-up option
            st.warning('Username does not exist. Please sign up.')

if __name__ == '__main__':
    login()
