from typing import Optional
import streamlit as st
import requests
from config import settings

BASE_URL = settings.base_url


def create_improvement(
        user_token: str, 
        code: str, 
        product_name: Optional[str], 
        brand: Optional[str], 
        image_front_url: Optional[str], 
        origins: Optional[str], 
        element_1: Optional[str], 
        material_1: Optional[str], 
        element_2: Optional[str], 
        material_2: Optional[str], 
        element_3: Optional[str], 
        material_3: Optional[str], 
        element_4: Optional[str], 
        material_4: Optional[str], 
        element_5: Optional[str], 
        material_5: Optional[str]):
    
    try:
        res = requests.post(f"{BASE_URL}/improvements/", json={
            "user_token": user_token, 
            "code": code, 
            "product_name": product_name, 
            "brand": brand, 
            "image_front_url": image_front_url, 
            "origins": origins, 
            "element_1": element_1, 
            "material_1": material_1, 
            "element_2": element_2, 
            "material_2": material_2, 
            "element_3": element_3, 
            "material_3": material_3, 
            "element_4": element_4, 
            "material_4": material_4, 
            "element_5": element_5, 
            "material_5": material_5
        }, headers={
            "Authorization": f"bearer {user_token}"
        })
        return {
            "status": res.status_code,
            "body": res.json()
        }
    except Exception as e:
        print(f"Failed to add improvement {e}")
        return {
            "status": res.status_code,
            "body": None
        }