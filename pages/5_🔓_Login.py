import streamlit as st 
from streamlit_api_client.auth_api import authenticate, logout

from menu import menu

menu()


style = "<style>h2 {text-align: center;} p {text-align: justify}</style>"
st.markdown(style, unsafe_allow_html=True)

st.header(":green[Authentication]")

if "auth_token" not in st.session_state:
    with st.form(key="auth_form", clear_on_submit=True):
        username = st.text_input(label="Please enter your email", max_chars=100, placeholder="user@example.com")
        password = st.text_input(label="Password", type="password")
        login = st.form_submit_button(label="Log in")

        if login and len(username) > 5 and len(password) > 1:
            # Attempt to authenticate
            with st.spinner('Authenticating...'):
                token = authenticate(username, password)

            if token:
                # If authentication successful, store token in session
                st.session_state.auth_token = token["token"]
                st.session_state.role = token["role"]
                st.rerun()
            else:
                st.toast("Failed to log in", icon="❌")
        elif login:
            st.toast("Please enter valid credentials", icon="⚠️")
else:
    if "role" in st.session_state and st.session_state.role == 'admin':
        st.success("You are currently authenticated as administrator.")
    else:
        st.success("You are currently authenticated as guest.")
    logout_btn = st.button(label="Log out")
    if logout_btn:
        logout()
