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


def login():
    users = fetch_users()
    emails = []
    usernames = []
    passwords = []

    for user in users:
        emails.append(user['key'])
        usernames.append(user['username'])
        passwords.append(user['password'])

    credentials = {'usernames': {}}
    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}

    Authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

    email, authentication_status, username = Authenticator.login(':green[log in]', 'main')

    info, info1 = st.columns(2)

    if not authentication_status:
        st.write("or")
        sign_up()

    if username:
        def current_user():
            return username
        if username in usernames:
            if authentication_status:
                # let User see app
                st.sidebar.subheader(f'hello {current_user()}!')
                Authenticator.logout('log out', 'sidebar')

                with st.sidebar:
                    selected = option_menu(
                        menu_title=None,
                        options=['home', 'diary','AI emotion detection','emotion bank','additional resources'],
                        icons=[':smile:',':angry','dont','work','pls',]
                    )
            
                if selected == 'home':
                    functions.home.fun()

                if selected == 'diary':
                    def diary():

                        pipe_lr = joblib.load(open("model/text_emotion.pkl", "rb"))

                        def predict_emotions(docx):
                            results = pipe_lr.predict([docx])
                            return results[0]

                        def get_prediction_proba(docx):
                            results = pipe_lr.predict_proba([docx])
                            return results

                        DETA_KEY = 'b0qtmrebnwh_2jMv8GoHJNL7VEBKUyfJcESigLbNHGkL'

                        deta = Deta(DETA_KEY)

                        db2 = deta.Base('diary')

                        user = current_user()
                    
                    
                    
                        def save_data(data):
                            current_date = datetime.now().strftime("%Y/%m/%d")
                            return db2.put({'username': user, 'key': current_date, 'text': data})


                        def get_data(user, date):
                            entries = db2.fetch().items
                            for entry in entries:
                                st.write(entry)
                                

                        def get_dates():
                            entries = db2.fetch().items
                            dates = [] 
                            for entry in entries:
                                if entry['username'] == user:
                                    dates.append(entry['key'])
                            st.write(dates)
                            return dates
                        
                        
                        def function():

                            st.title("Personal Diary :notebook:")

                            # access current date:
                            today_date = datetime.now().strftime("%m/%d/%Y")

                            # change view based on what menu button user clicks
                            selected = option_menu(
                                    menu_title=None,
                                    options=["today", "browse old entries"],
                                    orientation='horizontal',
                                    menu_icon='cast',
                                    icons=['','']
                            )


                            if selected=="today":
                                current_diary_entry = st.text_area("Today's Entry (" + today_date + "):", value=get_data(user,today_date))

                                if st.button("save"):
                                    # generate success message:
                                    success_message = st.success("saved.")
                                    time.sleep(1.5) # wait 2 seconds

                                    # THIS IS NEW : SETTING IN LOCAL STORAGE
                                    data = current_diary_entry
                                    save_data(data)
                                    success_message.empty()

                            elif selected=="browse old entries":
                                    st.title("select a date to view your entry and a prediction of your overall emotion")
                                    col1, col2 = st.columns(2)
                                    with col1:
                                        st.caption("date")
                                        dates = get_dates()
                                        for date in dates:
                                            if st.button(f"{date}"):
                                                st.write(get_data(user, date))
                                                with col2:
                                                    st.caption("mood")
                                                    prediction = predict_emotions(get_data(user,date))
                                                    probability = get_prediction_proba(get_data(user,date))
                                                    st.write("{}".format(prediction))
                                                    st.write("confidence: {}".format(np.max(probability)))


                                                    if st.button("close"):
                                                        pass
                                            


                        function()

                    if __name__=="__main__":
                        diary()

                if selected == 'AI emotion detection':
                    functions.ai.ai()
                if selected == 'emotion bank':
                    functions.emo.emo()
                if selected == 'additional resources':
                    functions.add.add()


            elif not authentication_status:
                with info:
                    st.error('Incorrect Password or username')
            else:
                with info:
                    st.warning('Please feed in your credentials')
        else:
            with info:
                st.warning('Username does not exist, Please Sign up')

    
if __name__ == '__main__':
    login()