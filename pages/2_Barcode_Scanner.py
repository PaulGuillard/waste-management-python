# https://discuss.streamlit.io/t/live-webcam-feed-into-the-web-app/397/2
# discussion about embedding the webcam in within streamlit framework
#

import streamlit as st
from front_utils import scanner as scanner, barcode_handler
# from Home import handle_barcode
# import Streamlit.Home as Home
import cv2
from menu import menu

menu()

style = "<style>h2 {text-align: center;} p {text-align: justify}</style>"
st.markdown(style, unsafe_allow_html=True)

st.header(":green[Scan any food product barcode]")

st.markdown("---")

def main():
    col1, col2, col3 = st.columns([6, 1, 6], gap="medium")
    if "searched_barcode" in st.session_state and st.session_state.searched_barcode != "":
        st.markdown("---")
        clear_btn = st.button(":orange[Clear data]")
        if clear_btn:
            del st.session_state['searched_barcode']
            st.rerun()
    
    col1.subheader(':green[Enter a barcode number manually]')
    col1.write("Unlock a multitude of recycling options by manually entering the barcode of any product.")

    if "searched_barcode" not in st.session_state:
        st.session_state.searched_barcode = ""
    if "searched_product_name" not in st.session_state:
        st.session_state.searched_product_name = ""
    if "searched_product_brand" not in st.session_state:
        st.session_state.searched_product_brand = ""
    if "searched_product_url" not in st.session_state:
        st.session_state.searched_product_url = ""
    if "searched_product_origins" not in st.session_state:
        st.session_state.searched_product_origins = ""


    barcode_manual = col1.text_input("Enter barcode:", value=st.session_state.searched_barcode)

    if barcode_manual:
        st.session_state.searched_barcode = ""
        barcode_handler.handle_barcode(barcode_manual)
    
    col2.header("OR")

    col3.subheader(':green[Scan a barcode with your camera]')
    col3.write("Simply use your device camera to scan the barcode of any product, and instantly display everything you need to know about your product.")
    
    subcol1, subcol2 = col3.columns(2)
    run = subcol1.button('Open camera')
    # camera = cv2.VideoCapture(0)
    # frame_window = st.image([])

    st.markdown("---")

    if run:
        with st.spinner("Loading barcode reader..."):
            camera = cv2.VideoCapture(0)
        frame_window = col3.image([])
        if subcol2.button('Close barcode scanner') and not barcode:
            run = not run
        barcode = scanner.read_barcode(run, camera, frame_window)
        barcode_handler.handle_barcode(barcode)
        frame_window.empty()

if __name__ == '__main__':
    main()
    
    

