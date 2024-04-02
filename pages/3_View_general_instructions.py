import streamlit as st 

from menu import menu

menu()

style = "<style>h2, h3 {text-align: center;} p {text-align: justify}</style>"
st.markdown(style, unsafe_allow_html=True)

st.header(":green[General Instructions]")

st.markdown("---")

st.image("images/general_recycling_instructions.PNG",use_column_width=True)