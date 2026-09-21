import requests
import streamlit as st

URL = "http://localhost:8000"

st.title("📚 Mini Bookstore")

# --- LOGIN SIDEBAR ---
st.sidebar.header("Login")
username = st.sidebar.text_input("Username")
password = st.sidebar.text_input("Password", type="password")

token = None
if st.sidebar.button("Login"):
    res = requests.post(f"{URL}/token", data={"username": username, "password": password})
    if res.status_code == 200:
        st.session_state["token"] = res.json()["access_token"]
        st.sidebar.success("Logged in!")
    else:
        st.sidebar.error("Wrong login info")

token = st.session_state.get("token")
headers = {"Authorization": f"Bearer {token}"} if token else {}


# --- 1. LIST BOOKS ---
st.subheader("📖 Books List")
try:
    res = requests.get(f"{URL}/books")
    if res.status_code == 200:
        for b in res.json():
            st.write(f"**ID {b['id']}**: {b['title']} — *Author:* {b['author']['name']} ({'Offer!' if b['is_offer'] else 'Regular'})")
except:
    st.error("Server not connected.")


st.divider()


# --- 2. ADD A BOOK ---
st.subheader("➕ Add a Book")
with st.form("add_form", clear_on_submit=True):
    b_id = st.number_input("Book ID", min_value=1, value=5)
    title = st.text_input("Title")
    
    st.write("--- Author Details ---")
    a_id = st.number_input("Author ID", min_value=1, value=5)
    a_name = st.text_input("Author Name")
    a_mail = st.text_input("Author Email")
    
    is_offer = st.checkbox("Special Offer?")
    
    if st.form_submit_button("Add Book"):
        if token:
            payload = {
                "id": b_id,
                "title": title,
                "author": {"id": a_id, "name": a_name, "mail": a_mail},
                "is_offer": is_offer
            }
            res = requests.post(f"{URL}/books", json=payload, headers=headers)
            if res.status_code in [200, 201]:
                st.success("Book added!")
                st.rerun()
            else:
                st.error(res.text)
        else:
            st.warning("Log in first from the sidebar!")