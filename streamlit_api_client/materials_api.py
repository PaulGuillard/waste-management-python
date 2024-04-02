import requests
from config import settings


BASE_URL = settings.base_url


def get_all_materials():
    try:
        res = requests.get(f"{BASE_URL}/materials/")
        return {
            "status": res.status_code,
            "body": res.json()
        }
    except Exception as e:
        print(f"Failed to fetch materials {e}")
        return {
            "status": res.status_code,
            "body": None
        }


def get_unvalidated_materials():
    all_materials = get_all_materials()
    unvalidated_materials = []
    for material in all_materials['body']:
        if not material['validated']:
            unvalidated_materials.append(material)
    return unvalidated_materials
    

def validate_material(id: int, raw_name: str, name: str, container_id: int, instructions: str, token: str):
    try:
        res = requests.put(f"{BASE_URL}/materials/{id}", json={
            "raw_name": raw_name,
            "name": name,
            "container_id": container_id,
            "instructions": instructions,
            "validated": True
            }, headers={
            "Authorization": f"bearer {token}"
        })
        return {
            "status": res.status_code,
            "body": res.json()
        }
    except Exception as e:
        print(f"Failed to validate material {e}")
        return {
            "status": res.status_code,
            "body": None
        }
    


def create_material(raw_name: str, name: str, container_id: int, instructions: str, token: str):
    try:
        res = requests.post(f"{BASE_URL}/materials/", json={
            "raw_name": raw_name,
            "name": name,
            "container_id": container_id,
            "instructions": instructions,
            "validated": True
        }, headers={
            "Authorization": f"bearer {token}"
        })
        return {
            "status": res.status_code,
            "body": res.json()
        }
    except Exception as e:
        print(f"Failed to create material {e}")
        return {
            "status": res.status_code,
            "body": None
        }
    

def update_material(id: int, raw_name: str, name: str, container_id: int, instructions: str, token: str):
    try:
        res = requests.put(f"{BASE_URL}/materials/{id}", json={
            "raw_name": raw_name,
            "name": name,
            "container_id": container_id,
            "instructions": instructions,
            "validated": True
            }, headers={
            "Authorization": f"bearer {token}"
        })
        return {
            "status": res.status_code,
            "body": res.json()
        }
    except Exception as e:
        print(f"Failed to update material {e}")
        return {
            "status": res.status_code,
            "body": None
        }
    

def delete_material(id: int, token: str):
    try:
        res = requests.delete(f"{BASE_URL}/materials/{id}", headers={
            "Authorization": f"bearer {token}"
        })
        return {
            "status": res.status_code,
            "body": None
        }
    except Exception as e:
        print(f"Failed to delete material {e}")
        return {
            "status": res.status_code,
            "body": None
        }