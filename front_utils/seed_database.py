import requests
from config import settings
import os
import json
import streamlit as st

def seed_containers(token):
    containers_req = requests.get(f"{settings.base_url}/containers")
    existing_containers = containers_req.json()

    with open("Streamlit" + os.sep + "data" + os.sep + "containers.json") as containers_file:
        new_containers = json.load(containers_file)
        try:
            for container in new_containers:
                # Check if container is already there
                already_there = False
                for existing_container in existing_containers:
                    if existing_container['name'] == container['name']:
                        already_there = True
                # If not there, add it to the DB
                if not already_there:
                    requests.post(f'{settings.base_url}/containers', json={
                        "name": container['name'],
                        "accepted": container['accepted'],
                        "not_accepted": container['not_accepted'],
                        "name_disp": container["name_disp"]
                    }, headers={
                        "Authorization": f"bearer {token}"
                    })
        except Exception as e:
            st.toast("❌ An issue occurred while updating the database...")
            st.write(f'{e}')
        else:
            st.toast("✅ The database was successfully updated!")


def seed_materials(token):
    containers = requests.get(f"{settings.base_url}/containers")
    existing_materials_req = requests.get(f"{settings.base_url}/materials")
    existing_materials = existing_materials_req.json()

    with open("Streamlit" + os.sep + "data" + os.sep + "materials.json") as materials_file:
        new_materials = json.load(materials_file)
        try:
            st.write("New materials written:")
            for material in new_materials:
                # Check if material is already there
                already_there = False
                for existing_material in existing_materials:
                    if existing_material['raw_name'] == material['name']:
                        already_there = True
                # If not, add it to database
                if not already_there:
                    container_id = None
                    for container in containers.json():
                        if container['name'].lower() == material['container_name'].lower():
                            container_id = container['id']
                    requests.post(f'{settings.base_url}/materials', json={
                        "raw_name": material['name'],
                        "name": material['eng_name'],
                        "container_id": container_id,
                        "instructions": material["instructions"]
                    }, headers={
                        "Authorization": f"bearer {token}"
                    })
                    st.write(material)
        except Exception as e:
            st.toast("❌ An issue occurred while updating the database...")
            st.write(f'{e}')
        else:
            st.toast("✅ The database was successfully updated!")