import streamlit as st 
from streamlit_api_client.auth_api import register, logout

from menu import menu

menu()

style = "<style>h2 {text-align: center;} p {text-align: justify}</style>"
st.markdown(style, unsafe_allow_html=True)

st.header(":green[Create an account]")

if "auth_token" not in st.session_state:
    with st.form(key="register_form", clear_on_submit=False):
        first_name = st.text_input(label="First Name", max_chars=50, placeholder="John")
        last_name = st.text_input(label="Last Name", max_chars=50, placeholder="Doe")
        email = st.text_input(label="Email", max_chars=75, placeholder="user@example.com")
        commune = st.selectbox(label="Commune", options=["Luxembourg", "Not Luxembourg"])
        password = st.text_input(label="Password (min length: 6 characters)", type="password")
        register_btn = st.form_submit_button(label="Register")

        if register_btn and len(email) > 5 and len(password) > 5:
            # Attempt to authenticate
            with st.spinner('Authenticating...'):
                token = register(first_name=first_name, last_name=last_name, email=email, commune=commune, password=password)

            if token:
                # If authentication successful, store token in session
                st.session_state.auth_token = token["token"]
                st.session_state.role = token["role"]
                st.rerun()
            else:
                st.toast("Failed to create an account", icon="❌")
        elif register_btn:
            st.toast("Please enter valid email and password", icon="⚠️")
else:
    st.success("You are now authenticated!")

    logout_btn = st.button(label="Log out")
    if logout_btn:
        logout()
