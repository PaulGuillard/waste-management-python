import streamlit as st
from menu import menu

st.set_page_config(page_title="Waste Management", layout="wide")

menu()

style = "<style>h2, h3 {text-align: center;} p {text-align: justify}</style>"
st.markdown(style, unsafe_allow_html=True)

# st.write(f"<h1 style='color:#17443e;'>Welcome to Waste Management & Local products App!</h1>", unsafe_allow_html=True) 
st.header(":green[Welcome to the first Waste Management App in Luxembourg!]")

st.markdown("---")

col1, col2 = st.columns([1, 3], gap="medium")
col1.write(" ")
col1.image("images/recycle-transparent-2.png")
col2.write(" #### Are you tired of constantly second-guessing which bin your waste should go in? Look no further.")
col2.write("This web application is designed specifically to help users in Luxembourg sort their waste with ease and precision. You can now bid farewell to the confusion of waste disposal and contribute to a cleaner and greener environment.")
col2.write("A simple scanning of a barcode is enough to start!")
col2.page_link(page="pages/2_Barcode_Scanner.py", label="#### :green[**♻️ Start scanning**]")

st.markdown("---")

st.subheader("How does it work?")

col1, col2, col3 = st.columns(3, gap="large")
col1.subheader(":green[SCAN]")
col1.write("Simply scan the barcode of any food product using your device camera or enter the barcode manually.")

col2.subheader(":green[CHECK INSTRUCTIONS]")
col2.write("Discover detailed recycling instructions for the item you scanned, instantly, as well as some extra information about the product.")

col3.subheader(":green[RECYCLE]")
col3.write("Contribute to a greener planet by recycling properly, based on the provided instructions.")

st.write(" ")
st.markdown("---")
st.write(" ")
st.subheader("MAKE A DIFFERENCE!")