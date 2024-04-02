import streamlit as st 
from front_utils.seed_database import seed_containers, seed_materials
from streamlit_api_client import containers_api, materials_api
from menu import menu_with_redirect

st.set_page_config(layout="wide")

menu_with_redirect()


# Stop if user is not admin
if "role" not in st.session_state or ("role" in st.session_state and st.session_state.role != 'admin'):
    st.warning("Only administrators can see the content of this page.")
    st.stop()  # App won't run anything after this line

tab_users, tab_containers, tab_materials, tab_operations = st.tabs(["Users", "Containers", "Materials", "General Operations"])

with tab_users:
    st.subheader("Users management")
    with st.expander(label="See users"):
        st.write("###### List of all users:")
        st.text("To be updated")
    
    with st.expander(label="Update users"):
        with st.form(key="user_update_form", clear_on_submit=True):
            st.number_input("Please enter the user id:", min_value=1)
            find_user = st.form_submit_button("Find user")
            if find_user:
                st.write("Display form for the user update, pre-populated")

    with st.expander(label="Delete users"):
        with st.form(key="user_delete_form", clear_on_submit=True):
            st.number_input("Please enter the user id:", min_value=1)
            find_user_to_delete = st.form_submit_button("Find user")
            if find_user_to_delete:
                st.write("Display confirmation for user delete")

        
with tab_containers:
    st.subheader("Containers management")
    with st.expander(label="See containers"):
        list_containers_btn = st.button("Refresh list")
        if list_containers_btn:
            st.write("###### List of all containers:")
            all_containers = containers_api.get_all_containers()
            if all_containers['status'] != 200:
                st.warning("Could not fetch containers information...")
            else:
                st.dataframe(
                    all_containers["body"], 
                    hide_index=True, 
                    column_order=["id", "name_disp", "name", "accepted", "not_accepted"], 
                    column_config={
                        "id": "ID",
                        "name_disp": "Display name", 
                        "name": "Generic name", 
                        "accepted": "Accepted items", 
                        "not_accepted": "Not accepted items"
                    }
                )
                

    with st.expander(label="Create containers"):
        with st.form(key="container_create_form", clear_on_submit=True):
            create_container_name = st.text_input("Container name")
            create_container_disp_name = st.text_input("Container display name")
            create_container_accepted = st.text_input("Accepted: (Separated by comma)", placeholder="item1,item2,item3,...") 
            create_container_not_accepted = st.text_input("Not accepted: (Separated by comma)", placeholder="item1,item2,item3,...") 
            create_container_btn = st.form_submit_button("Create container")
            if create_container_btn:
                created_container = containers_api.create_container(
                    name=create_container_name,
                    display_name=create_container_disp_name,
                    accepted=create_container_accepted,
                    not_accepted=create_container_not_accepted,
                    token=st.session_state.auth_token
                )
                if created_container['status'] == 201:
                    st.toast("✅ :green[New container successfully created!]")
                else:
                    st.toast("❌ :red[New container could not be created... Please try again.]")
        

    with st.expander(label="Update containers"):
        container_id_to_update = st.number_input("Please enter the container id:", min_value=0, key="update_container_id")
        find_container = st.button("Find container")
        if find_container:
            st.session_state.updated_container_id = container_id_to_update
        if "updated_container_id" in st.session_state and container_id_to_update > 0:
            container_to_update = containers_api.get_specific_container(st.session_state.updated_container_id)
            if container_to_update['status'] != 200:
                st.warning("Could not find this container in our records. Please try with another value.")
            else:
                with st.form(key="container_update_form", clear_on_submit=False):
                    update_container_name = st.text_input("Container name", value=container_to_update['body']['name'])
                    update_container_disp_name = st.text_input("Container display name", value=container_to_update['body']['name_disp'])
                    update_accepted_str = ",".join(container_to_update['body']['accepted'])
                    update_container_accepted = st.text_input("Accepted: (Separated by comma)", value=update_accepted_str)
                    update_not_accepted_str = ",".join(container_to_update['body']['not_accepted'])
                    update_container_not_accepted = st.text_input("Not accepted: (Separated by comma)", value=update_not_accepted_str) 
                    update_container_btn = st.form_submit_button("Update container")
                    if update_container_btn:
                        updated_container = containers_api.update_container(
                            id=st.session_state.updated_container_id,
                            name=update_container_name,
                            display_name=update_container_disp_name,
                            accepted=update_container_accepted,
                            not_accepted=update_container_not_accepted,
                            token=st.session_state.auth_token
                        )
                        if updated_container['status'] == 200:
                            st.toast("✅ :green[New container successfully updated!]")
                            del st.session_state["updated_container_id"]
                        else:
                            st.toast("❌ :red[New container could not be updated... Please try again.]")
                

    with st.expander(label="Delete containers"):
        container_id_to_delete = st.number_input("Please enter the container id:", min_value=1)
        delete_container_btn = st.button("⚠️ Delete container", type="primary")
        if delete_container_btn:
            container_deleted = containers_api.delete_container(container_id_to_delete, st.session_state.auth_token)
            if container_deleted['status'] == 204:
                st.toast("✅ :green[Container successfully deleted!]")
            else:
                st.toast("❌ :red[The container could not be deleted... Please try again]")


if "validated_material" in st.session_state:
    st.toast(f"✅ :green[{st.session_state.validated_material}]")
    del st.session_state['validated_material']
if "updated_material" in st.session_state:
    st.toast(f"✅ :green[{st.session_state.updated_material}]")
    del st.session_state['updated_material']

with tab_materials:
    # Create containers list for selectboxes in all material operations
    validate_materials_container_options_req = containers_api.get_all_containers()
    validate_materials_container_options = ['None']
    for option in validate_materials_container_options_req['body']:
        validate_materials_container_options.append(option['name_disp'])

    st.subheader("Materials management")

    # Display all materials in the database
    with st.expander(label="See all materials"):
        list_materials_btn = st.button("Refresh list", key="list_materials_refresh_btn")
        if list_materials_btn:
            st.write("###### List of all materials:")
            all_materials = materials_api.get_all_materials()
            if all_materials['status'] != 200:
                st.warning("Could not fetch materials information...")
            else:
                st.dataframe(
                    all_materials["body"], 
                    hide_index=True, 
                    column_order=["id", "validated", "raw_name", "name", "instructions", "container_id", "container"], 
                    column_config={
                        "id": "ID",
                        "validated": "Validated?",
                        "raw_name": "Original name", 
                        "name": "Generic name", 
                        "instructions": "Instructions", 
                        "container_id": "Container ID",
                        "container": "Container details"
                    }
                )

    # Validate materials which were automatically added to the database
    # so they can be displayed on the front-end in the future
    with st.expander(label="Validate materials", expanded=True):
        unvalidated_materials = materials_api.get_unvalidated_materials()
        if len(unvalidated_materials) == 0:
            st.write("All materials have already been validated!")
        else:
            for unvalidated_material in unvalidated_materials:
                key = f"unvalidated_material_update_{unvalidated_material['id']}"
                with st.form(key=key):
                    st.write(f"##### Material original name: :orange[{unvalidated_material['raw_name']}]")
                    validate_material_name = st.text_input("Material display name")
                    validate_material_instructions = st.text_area(label="Specific instructions for this material", max_chars=500)
                    validate_material_container_name = st.selectbox(label="Select appropriate container", options=validate_materials_container_options)
                    validate_material_btn = st.form_submit_button("Validate material")
                    if validate_material_btn:
                        validate_material_container_id = None
                        for option in validate_materials_container_options_req['body']:
                            if option['name_disp'] == validate_material_container_name:
                                validate_material_container_id = option['id']
                        validated_material = materials_api.validate_material(
                            id=unvalidated_material['id'],
                            raw_name=unvalidated_material['raw_name'],
                            name=validate_material_name,
                            container_id=validate_material_container_id,
                            instructions=validate_material_instructions,
                            token=st.session_state.auth_token
                        )
                        if validated_material['status'] == 200:
                            unvalidated_materials = materials_api.get_unvalidated_materials()
                            st.session_state.validated_material = f"Material {validate_material_name} successfully validated!"
                            st.rerun()
                        else:
                            st.toast("❌ :red[Material could not be validated... Please try again.]")


    with st.expander(label="Update materials"):
        all_materials = materials_api.get_all_materials()
        if len(all_materials) == 0:
            st.write("No materials in the list for the moment...")
        else:
            for updated_material in all_materials["body"]:
                key = f"updated_material_update_{updated_material['id']}"
                with st.form(key=key):
                    st.write(f"##### Material original name: :orange[{updated_material['raw_name']}]")
                    updated_material_name = st.text_input("Material display name", value=updated_material['name'])
                    updated_material_instructions = st.text_area(label="Specific instructions for this material", max_chars=500, value=updated_material['instructions'])
                    if updated_material['container_id']:
                        updated_material_container_name = st.selectbox(label="Select appropriate container", options=validate_materials_container_options, index=validate_materials_container_options.index(updated_material['container']['name_disp']))
                    else:
                        updated_material_container_name = st.selectbox(label="Select appropriate container", options=validate_materials_container_options, index=0)
                    updated_material_btn = st.form_submit_button("Update material")
                    if updated_material_btn:
                        updated_material_container_id = None
                        for option in validate_materials_container_options_req['body']:
                            if option['name_disp'] == updated_material_container_name:
                                updated_material_container_id = option['id']
                        updated_material = materials_api.update_material(
                            id=updated_material['id'],
                            raw_name=updated_material['raw_name'],
                            name=updated_material_name,
                            container_id=updated_material_container_id,
                            instructions=updated_material_instructions,
                            token=st.session_state.auth_token
                        )
                        if updated_material['status'] == 200:
                            all_materials = materials_api.get_all_materials()
                            st.session_state.updated_material = f"Material {updated_material_name} successfully updated!"
                            st.rerun()
                        else:
                            st.toast("❌ :red[Material could not be updated... Please try again.]")


    # Delete materials, including relationships with products
    with st.expander(label="Delete materials"):
        material_id_to_delete = st.number_input("Please enter the material id:", min_value=1)
        delete_material_btn = st.button("⚠️ Delete material", type="primary")
        if delete_material_btn:
            material_deleted = materials_api.delete_material(material_id_to_delete, st.session_state.auth_token)
            if material_deleted['status'] == 204:
                st.toast("✅ :green[Material successfully deleted!]")
            else:
                st.toast("❌ :red[The material could not be deleted... Please try again]")


with tab_operations:
    # Specific operations related to website administration
    st.subheader("Click to seed the database with initialization data")
    col1, col2 = st.columns(2)

    if col1.button(label="Import containers and materials"):
        seed_containers(st.session_state.auth_token)
        seed_materials(st.session_state.auth_token)

        

