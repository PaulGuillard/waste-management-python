import streamlit as st
from streamlit_api_client import improvements_api

from menu import menu_with_redirect

menu_with_redirect()

st.header("Provide product info")
st.write("We need your help to improve the quality of our data!")
st.write("")

if "auth_token" not in st.session_state:
    st.warning("You need to be logged in to see this page...")
    st.page_link("pages/5_🔓_Login.py", label="Go to login page")
    st.stop()


if "searched_barcode" not in st.session_state:
    st.warning("Please search for a barcode on the home page first!")
    st.page_link("Home.py", label="Go to home page")
    st.stop()

# Product Code
st.write(f"###### Barcode: {st.session_state.searched_barcode}")

with st.form(key="product_improvement_form"):
    product_name = st.text_input("Product name", key="product_name", value=st.session_state.searched_product_name)
    brand = st.text_input("Product brand", placeholder="Nestlé, Danone, ...", key="brand", value=st.session_state.searched_product_brand)
    image_front_url = st.text_input("Picture URL", placeholder="https://www.images.com/12345.png", key="image_url", value=st.session_state.searched_product_url)
    origins = st.text_input("Product origins", placeholder="Luxembourg, France, Germany, Belgium, ...", key="origins", value=st.session_state.searched_product_origins)
    
    col1, col2 = st.columns(2)
    element_1 = col1.text_input("Packaging element or shape", placeholder="Bottle, jar, lid, seal, ...", key="element1")
    material_1 = col2.text_input("Corresponding material", placeholder="Glass, paper, plastic, ...", key="material1")
    col1.write(" ")
    col2.write(" ")

    element_2 = col1.text_input("Packaging element or shape", placeholder="Bottle, jar, lid, seal, ...", key="element2")
    material_2 = col2.text_input("Corresponding material", placeholder="Glass, paper, plastic, ...", key="material2")
    col1.write(" ")
    col2.write(" ")

    element_3 = col1.text_input("Packaging element or shape", placeholder="Bottle, jar, lid, seal, ...", key="element3")
    material_3 = col2.text_input("Corresponding material", placeholder="Glass, paper, plastic, ...", key="material3")
    col1.write(" ")
    col2.write(" ")

    element_4 = col1.text_input("Packaging element or shape", placeholder="Bottle, jar, lid, seal, ...", key="element4")
    material_4 = col2.text_input("Corresponding material", placeholder="Glass, paper, plastic, ...", key="material4")
    col1.write(" ")
    col2.write(" ")

    element_5 = col1.text_input("Packaging element or shape", placeholder="Bottle, jar, lid, seal, ...", key="element5")
    material_5 = col2.text_input("Corresponding material", placeholder="Glass, paper, plastic, ...", key="material5")
    col1.write(" ")
    col2.write(" ")

    improvement_form_btn = st.form_submit_button(label="Send product updates")
    if improvement_form_btn:
        improvement_creation_req = improvements_api.create_improvement(
            user_token=st.session_state.auth_token,
            code=st.session_state.searched_barcode,
            product_name=product_name,
            brand=brand,
            image_front_url=image_front_url,
            origins=origins,
            element_1=element_1,
            material_1=material_1,
            element_2=element_2,
            material_2=material_2,
            element_3=element_3,
            material_3=material_3,
            element_4=element_4,
            material_4=material_4,
            element_5=element_5,
            material_5=material_5
        )
        if improvement_creation_req['status'] != 201:
            st.toast("❌ :red[An unexpected issue occurred, we could not save the information... Please try again.]")
        else:
            st.toast("✅ :green[Your suggestion was successfully saved, thank you!]")
            del st.session_state.searched_barcode
            del st.session_state.searched_product_name
            del st.session_state.searched_product_brand
            del st.session_state.searched_product_url
            del st.session_state.searched_product_origins
            st.success("Thank you! We will review this information and send it to openfoodfacts.org!")
