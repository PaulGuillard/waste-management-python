import streamlit as st
import requests
from config import settings

BASE_URL = settings.base_url


def get_all_containers():
    try:
        res = requests.get(f"{BASE_URL}/containers/")
        return {
            "status": res.status_code,
            "body": res.json()
        }
    except Exception as e:
        print(f"Failed to fetch containers {e}")
        return {
            "status": res.status_code,
            "body": None
        }
    

def get_specific_container(id: int):
    try:
        res = requests.get(f"{BASE_URL}/containers/{id}")
        return {
            "status": res.status_code,
            "body": res.json()
        }
    except Exception as e:
        print(f"Failed to fetch container {e}")
        return {
            "status": res.status_code,
            "body": None
        }
        

def create_container(name: str, display_name: str, accepted: str, not_accepted: str, token: str):
    accepted_list = accepted.split(",")
    not_accepted_list = not_accepted.split(",")
    try:
        res = requests.post(f"{BASE_URL}/containers/", json={
            "name": name,
            "name_disp": display_name,
            "accepted": accepted_list,
            "not_accepted": not_accepted_list
        }, headers={
            "Authorization": f"bearer {token}"
        })
        return {
            "status": res.status_code,
            "body": res.json()
        }
    except Exception as e:
        print(f"Failed to create container {e}")
        return {
            "status": res.status_code,
            "body": None
        }
    

def update_container(id: int, name: str, display_name: str, accepted: str, not_accepted: str, token: str):
    accepted_list = accepted.split(",")
    not_accepted_list = not_accepted.split(",")
    try:
        res = requests.put(f"{BASE_URL}/containers/{id}", json={
            "name": name,
            "name_disp": display_name,
            "accepted": accepted_list,
            "not_accepted": not_accepted_list
        }, headers={
            "Authorization": f"bearer {token}"
        })
        return {
            "status": res.status_code,
            "body": res.json()
        }
    except Exception as e:
        print(f"Failed to update container {e}")
        return {
            "status": res.status_code,
            "body": None
        }
    

def delete_container(id: int, token: str):
    try:
        res = requests.delete(f"{BASE_URL}/containers/{id}", headers={
            "Authorization": f"bearer {token}"
        })
        return {
            "status": res.status_code,
            "body": None
        }
    except Exception as e:
        print(f"Failed to delete container {e}")
        return {
            "status": res.status_code,
            "body": None
        }