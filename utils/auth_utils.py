# utils/auth_utils.py

import requests
import streamlit as st

FIREBASE_API_KEY = st.secrets["FIREBASE_API_KEY"]
AUTH_URL = st.secrets["FIREBASE_AUTH_URL"]

def sign_in_with_email_password(email, password):
    url = f"{AUTH_URL}:signInWithPassword?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    res = requests.post(url, json=payload)
    if res.status_code == 200:
        return res.json()
    else:
        return None

def sign_up(email, password):
    url = f"{AUTH_URL}:signUp?key={FIREBASE_API_KEY}"
    payload = {"email": email, "password": password, "returnSecureToken": True}
    res = requests.post(url, json=payload)
    return res.ok
