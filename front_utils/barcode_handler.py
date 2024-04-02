import streamlit as st
import requests
from config import settings

def handle_barcode(barcode: str):
    # Mapping of keys to their display names
    DISPLAY_NAMES = {
        'image_front_url': 'Image',
        'product_name': '**Product name**',
        'brands': '**Brand**',
        'package_materials' : '**Package materials**',     
        'manufacturing_places': '**Manufacturing**'
    }

    CONTAINER_PICTURES = {
        'Paper/Cardboard': 'paper_waste.png',
        'Glass': 'glass_waste.png',
        'Valorlux (blue bag)': 'valorlux.png',
        'Mixed residual waste': 'general_waste.png',
        'Recycling center': 'recycling_center.png'
    }

    if barcode:
        st.session_state.searched_barcode = barcode.strip()

        product_data_req = requests.get(f"{settings.base_url}/products/{barcode}")
        status_code = product_data_req.status_code
        if status_code >= 500:
            st.write("Sorry, an internal error occurred... Please try again later.")
        elif status_code >= 400:
            st.write("Product could not be found... Please try again with another barcode.")
            st.write(" ")
            st.subheader(":green[Do you have information about this product?]")
            st.write("Click on the link below to provide missing information about this product:")
            st.page_link("pages/4_Add_product_info.py", label=":green[**Add missing information**]")
        else:
            product_data = product_data_req.json()

            if product_data:
                st.session_state.searched_product_name = product_data['product_name']
                st.session_state.searched_product_brand = product_data['brands']
                st.session_state.searched_product_url = product_data['image_front_url']
                st.session_state.searched_product_origins = ", ".join(product_data['origins']).replace("en:", "")

                st.header(":green[Product Information]")
                st.write("# ")
                # General product information
                # Iterate over the keys in DISPLAY_NAMES
                col1, col2 = st.columns([3, 9], gap="medium")
                col2.write("##### :green[Product Details:]")
                for key in DISPLAY_NAMES:
                    # Check if the key exists in product_data
                    if key in product_data:
                        value = product_data[key]
                        display_name = DISPLAY_NAMES[key]
                        # If value is a list, join its elements into a single string
                        if isinstance(value, list):
                            value = ", ".join(value)
                        if key == 'image_front_url':
                            if value != 'N/A':
                                col1.image(value, caption=product_data['product_name'], use_column_width=True)
                            else:
                                col1.write(f"{display_name}: {value}")
                        # Skip displaying 'Package elements' if it is 'N/A'
                        elif key == 'Package_elements' and value == 'N/A':
                            continue
                        else:
                            col2.write(f"{display_name}: {value}")
                
                # Local origin check
                if product_data['origins'] and product_data['origins'] != "N/A":
                    col2.write(" ")
                    col2.write("##### :green[Product Origins:]")
                    if type(product_data['origins']) == list:
                        local_level = 0
                        for origin in product_data['origins']:
                            if origin.find("luxemb") > -1:
                                local_level = 2
                            elif origin.find("fran") > -1 or origin.find("belg") > -1 or origin.find("germ") > -1:
                                local_level = 1
                        if local_level == 0:
                            col2.write("👎 :red[Not local...]")
                        elif local_level == 1:
                            col2.write(":orange[Produced in nearby countries]")
                        else:
                            col2.write("👍 :green[Produced locally!]")

                col2.write(" ")
                col2.write("##### :green[Contribute:]")
                col2.write("Any information missing or incorrect? You can do something about it! Help us improve the results by clicking on the link below, to provide missing information about this product!")
                col2.page_link("pages/4_Add_product_info.py", label="**Add missing information**", use_container_width=False)       

                # Recycling instructions
                st.write(" ")
                st.header(":green[Recycling instructions]")
                st.write(" ")
                if product_data['instructions']['status'] in ["nok", "missing"]: # if an issue occurred while fetching instructions
                    st.write("Unfortunately, the packaging information has not yet been provided for this product. Please follow the general instructions to dispose of this package.")

                    if product_data["instructions"]["error"]:
                        st.warning(product_data["instructions"]["error"])
                    
                    #st.write("##### Check general instructions:")
                    st.page_link("pages/3_View_general_instructions.py", label="**View general instructions**")
                    st.write("")
                    st.write("Your effort is greatly appreciated in helping to create a more sustainable environment for us all!")    
                else: # if there are instructions
                    if len(product_data["instructions"]) == 3:
                        # Case only one type of packaging
                        for key, instruction in product_data["instructions"].items(): # print each instruction
                            if key not in ['status', 'error']:
                                if instruction["container"] == 'unknown':
                                    st.markdown("---")
                                    wastecol1, wastecol2 = st.columns([2, 10], gap="medium")
                                    wastecol1.image(f"images/question.png", use_column_width=True)
                                    wastecol2.write("#### :green[Not available...]")
                                    wastecol2.write(f"> Unfortunately, the packaging information has not yet been provided for this product. Please follow the general instructions to dispose of this package.")
                                    wastecol2.page_link("pages/3_View_general_instructions.py", label="**View general instructions**")
                                    st.markdown("---")
                                    # st.write(f"> Unfortunately, the packaging information has not yet been provided for this product. Please follow the general instructions to dispose of this package.")
                                    #st.write("##### Check general instructions:")
                                    # st.page_link("pages/3_View_general_instructions.py", label="**View general instructions**")
                                    # st.write("")
                                else:
                                    st.markdown("---")
                                    wastecol1, wastecol2 = st.columns([2, 10], gap="medium")
                                    wastecol1.image(f"images/{CONTAINER_PICTURES[instruction['container']]}", use_column_width=True)
                                    wastecol2.write("#### :green[Whole product]")
                                    wastecol2.write(f"Please dispose of the whole product in the **{instruction["container"]}** container.")
                                    wastecol2.write("###### ℹ️ Extra tip:")
                                    wastecol2.write(f"_{instruction['material_instructions']}_")
                                    st.markdown("---")
                                    # st.write(f"> Please dispose of the whole product in the **{instruction["container"]}** container.")
                                    # st.warning(f"ℹ️ {instruction['material_instructions']}")
                                st.write("Thank you for your commitment to recycling! Your effort is greatly appreciated in helping to create a more sustainable environment for us all!")
                    else:
                        # Get the package elements
                        for material, instruction in product_data["instructions"].items(): # print each instruction
                            if material not in ['status', 'error']:
                                elements = instruction["shapes"].split(",")
                                if len(elements) > 2:
                                    elements_to_separate = ', '.join(elements[0:-1]) + f" and {elements[-1]}"
                                # If there are exactly two elements, join them with 'and'
                                elif len(elements) == 2:
                                    elements_to_separate = ' and '.join(elements)
                                # If there is only one element or none, no need to separate
                                else:
                                    elements_to_separate = elements[0]

                                # Print the message
                                # st.write(f" Please remember to separate the {elements_to_separate} to ensure they can be properly recycled.")

                                container = instruction["container"]
                                if container == 'unknown':
                                    st.markdown("---")
                                    wastecol1, wastecol2 = st.columns([2, 10], gap="medium")
                                    wastecol1.image("images/question.png", use_column_width=True)
                                    wastecol2.write(f"#### :green[Data not available...]")
                                    wastecol2.write(f"Unfortunately, material details for {elements_to_separate} are not available at the moment. To dispose of them correctly, please follow the general instructions:")
                                    wastecol2.page_link("pages/3_View_general_instructions.py", label="_View general instructions_")
                                    # st.write(f"Unfortunately, material details for {elements_to_separate} are not available at the moment. To dispose of them correctly, please follow the general instructions:")
                                    # st.page_link("pages/3_View_general_instructions.py", label="_View general instructions_")
                                    # st.write("")
                                else:
                                    st.markdown("---")
                                    wastecol1, wastecol2 = st.columns([3, 9], gap="medium")
                                    wastecol1.image(f"images/{CONTAINER_PICTURES[container]}", use_column_width=True)
                                    wastecol2.write(f"#### :green[{material} {elements_to_separate}]")
                                    wastecol2.write(f"Dispose of the **{material} {elements_to_separate}** in the **{container}** container.")
                                    wastecol2.write("###### ℹ️ Extra tip:")
                                    wastecol2.write(f"_{instruction['material_instructions']}_")
                                    # st.markdown("---")
                                    # st.write(f"> Dispose of the **{material} {elements_to_separate}** in the **{container}** container.")
                                    # st.warning(f"ℹ️ {instruction['material_instructions']}")

                        st.markdown("---")
                        st.write("Thank you for your commitment to recycling! Your effort is greatly appreciated in helping to create a more sustainable environment for us all!")
