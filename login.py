# login.py

import streamlit as st
from auth.auth_manager import login, is_logged_in, get_current_user, logout

def show_login():
    st.title("🔐 Login to AI Job Assistant")

    if is_logged_in():
        st.success(f"Logged in as {get_current_user()}")
        if st.button("Logout"):
            logout()
            st.experimental_rerun()
        return True

    st.subheader("Enter your credentials")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email or not password:
            st.warning("Please enter both email and password.")
        else:
            with st.spinner("Authenticating..."):
                success, message = login(email, password)
                if success:
                    st.success("✅ Login successful")
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
    return False
