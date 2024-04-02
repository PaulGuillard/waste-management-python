import streamlit as st

def authenticated_menu():
    st.sidebar.subheader("Welcome!")
    st.sidebar.page_link("Home.py", label="🪴 Home")
    st.sidebar.page_link("pages/2_Barcode_Scanner.py", label="🔍 Scan a product")
    st.sidebar.page_link("pages/3_View_general_instructions.py", label="📄 View general instructions")
    st.sidebar.page_link("pages/4_Add_product_info.py", label="➕ Contribute")
    if "role" in st.session_state and st.session_state.role == 'admin':
        st.sidebar.page_link("pages/9_🛂_Admin_panel.py", label="🛂 Admin Panel")
    st.sidebar.page_link("pages/5_🔓_Login.py", label="🔓 Logout")


def unauthenticated_menu():
    # Show a navigation menu for unauthenticated users
    st.sidebar.subheader("Welcome!")
    st.sidebar.page_link("Home.py", label="🪴 Home")
    st.sidebar.page_link("pages/2_Barcode_Scanner.py", label="🔍 Scan a product")
    st.sidebar.page_link("pages/3_View_general_instructions.py", label="📄 View general instructions")
    st.sidebar.page_link("pages/5_🔓_Login.py", label="🔓 Login")
    st.sidebar.page_link("pages/6_👤_Register.py", label="👤 Register")


def menu():
    # Determine if a user is logged in or not, then show the correct
    # navigation menu
    if "auth_token" not in st.session_state:
        unauthenticated_menu()
        return
    authenticated_menu()


def menu_with_redirect():
    # Redirect users to the main page if not logged in, otherwise continue to
    # render the navigation menu
    if "role" not in st.session_state or st.session_state.role is None:
        st.switch_page("pages/5_🔓_Login.py")
    menu()