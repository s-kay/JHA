# auth/auth_manager.py

import streamlit as st
import requests

def login(email, password):
    try:
        res = requests.post(st.secrets["FIREBASE_AUTH_URL"], json={"email": email, "password": password})
        res.raise_for_status()
        token = res.json().get("idToken")
        st.session_state["auth_token"] = token
        st.session_state["user_email"] = email
        return True, "Login successful"
    except requests.exceptions.RequestException as e:
        return False, str(e)

def logout():
    st.session_state.pop("auth_token", None)
    st.session_state.pop("user_email", None)

def is_logged_in():
    return "auth_token" in st.session_state

def get_current_user():
    return st.session_state.get("user_email", None)
