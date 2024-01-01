import pytz
import streamlit as st
import streamlit_authenticator as stauth
from deps import sign_up, fetch_users

import joblib
import numpy as np
from datetime import datetime
from streamlit_option_menu import option_menu
from deta import Deta

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
    usernames = [user['username'] for user in users]

    entered_username = st.text_input("Enter your username:")

    if st.button("Log In"):
        if entered_username in usernames:
            authentication_status, authenticated_username = authenticate_user(entered_username, users)

            if authentication_status:
                # User successfully authenticated
                st.sidebar.subheader(f'Hello {authenticated_username}!')
                # Continue with the rest of your app logic

                with st.sidebar:
                    selected = option_menu(
                        menu_title=None,
                        options=['home', 'diary', 'AI emotion detection', 'emotion bank', 'additional resources'],
                        icons=[':smile:', ':angry', 'dont', 'work', 'pls', ]
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

                            user = authenticated_username

                            def save_data(data):
                                current_date = datetime.now(pytz.timezone('US/Pacific')).strftime("%Y/%m/%d")
                                dates = get_dates()
                                if current_date in dates:
                                    updates = {"text": data}
                                    db2.update(updates, current_date)

                                if current_date not in dates:
                                    db2.put({'username': user, 'text': data}, current_date)

                            def get_data(user, date):
                                entries = db2.fetch().items
                                for entry in entries:
                                    if entry['username'] == user and entry['key'] == date and entry.get('text') is not None:
                                        return entry.get('text')
                                return ""

                            def get_dates():
                                entries = db2.fetch().items
                                dates = []
                                for entry in entries:
                                    if entry['username'] == user:
                                        dates.append(entry['key'])

                                return dates

                            def function():
                                st.title("Personal Diary :notebook:")

                                # access current date:
                                today_date = datetime.now(pytz.timezone('US/Pacific')).strftime("%Y/%m/%d")

                                # change view based on what menu button user clicks
                                selected = option_menu(
                                    menu_title=None,
                                    options=["today", "browse old entries"],
                                    orientation='horizontal',
                                    menu_icon='cast',
                                    icons=['', '']
                                )

                                if selected == "today":
                                    current_diary_entry = st.text_area(
                                        "Today's Entry (" + today_date + "):", value=get_data(user, today_date))

                                    if st.button("save"):
                                        # generate success message:
                                        success_message = st.success("saved.")
                                        time.sleep(1.5)  # wait 2 seconds

                                        # THIS IS NEW : SETTING IN LOCAL STORAGE
                                        data = current_diary_entry
                                        save_data(data)
                                        success_message.empty()

                                elif selected == "browse old entries":
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
                                                    prediction = predict_emotions(get_data(user, date))
                                                    probability = get_prediction_proba(get_data(user, date))
                                                    st.write("{}".format(prediction))
                                                    st.write("confidence: {}".format(np.max(probability)))

                                                    if st.button("close"):
                                                        pass

                            function()

                        if __name__ == "__main__":
                            diary()

                    if selected == 'AI emotion detection':
                        functions.ai.ai()
                    if selected == 'emotion bank':
                        functions.emo.emo()
                    if selected == 'additional resources':
                        functions.add.add()

            elif not authentication_status:
                st.error('Incorrect password for the username')
            else:
                st.warning('Please enter your credentials')

        else:
            # Username not found in the database, show sign-up option
            sign_up()
            st.warning('Username does not exist, please sign up.')


if __name__ == '__main__':
    login()
