import streamlit as st

st.set_page_config(
    page_title="Smart Route Planner",
    layout="wide",
    initial_sidebar_state="expanded"   # 👈 ADD THIS
)

st.markdown("""
### Welcome 👋  

This project includes:

- 📊 **Basic Graph Planner** (Dijkstra & A*)
- 🗺️ **Real Map Planner** (OSM-based routing)

👉 Use the sidebar to navigate
""")
st.title("🌍 Smart Route Planner")