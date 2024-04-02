import streamlit as st
import requests
from config import settings

BASE_URL = settings.base_url


def logout():
    del st.session_state.auth_token
    del st.session_state.role
    st.rerun()


def authenticate(username: str, password: str):
    # Authenticate with the backend and get a token
    try:
        # POST request to the /auth/login endpoint
        res = requests.post(f"{settings.base_url}/auth/login", data={
            "username": username,
            "password": password
        })
        return {
            "token": res.json()["access_token"],
            "role": res.json()["role"],
        }
    except Exception as e:
        print(f"Authentication failed! {e}")
        return None


def register(first_name: str, last_name: str, email: str, commune: str, password: str):
    # Authenticate with the backend and get a token
    try:
        # POST request to the /auth/login endpoint
        res = requests.post(f"{settings.base_url}/auth/register", json={
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "commune": commune,
            "password": password
        })
        return {
            "token": res.json()["access_token"],
            "role": res.json()["role"],
        }
    except Exception as e:
        print(f"Registration failed! {e}")
        return None  

