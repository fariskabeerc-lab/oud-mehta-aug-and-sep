import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Setup (must be first) ---
st.set_page_config(page_title="Sales Insights Dashboard", layout="wide")

# --- Authentication Setup ---
def login():
    st.title("🔐 Login to Sales Insights Dashboard")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "almadina" and password == "12345":
            st.session_state["authenticated"] = True
            st.success("✅ Login successful! Access granted.")
            st.rerun()
        else:
            st.error("❌ Invalid username or password")

# --- Run Login Check ---
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

if not st.session_state["authenticated"]:
    login()
    st.stop()

# ===========================================================
# --- Dashboard Code (only runs after login) ---
# ===========================================================

st.title("📊SAFA oud mehta AUG&SEP Sales Insights")

# --- Load Data ---
df = pd.read_excel("sales of oud mehta aug and sep.Xlsx")   # change filename if needed
