import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום", layout="centered")

# הגדרת צבעים (לפי הלוגו הכתום)
color_orange = "#E65100" 
color_light_grey = "#F2F2F2" 
color_dark_grey = "#333333" 

# עיצוב CSS - פונט Assistant, יישור לימין וצבע פלוס כתום
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    
    /* פונט Assistant ויישור לימין לכל האפליקציה */
    html, body, [class*="css"], .stApp {{
        font-family: 'Assistant', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }}
    
    /* הפיכת הפלוס והטקסט ב-Expander לכתום */
    .streamlit-expanderHeader {{
        color: {color_orange} !important;
        fill: {color_orange} !important; /* צובע את האייקון של הפלוס */
        font-weight: bold !important;
    }}

    /* עיצוב שדות קלט אפורים עם פונט Assistant */
    input {{
        background-color: {color_light_grey} !important;
        color: {color_dark_grey} !important;
        font-family: 'Assistant', sans-serif !important;
    }}

    /* כפתור שמירה כתום */
    div.stButton > button {{
        background-color: {color_orange} !important;
        color: white !important;
        font-family: 'Assistant', sans-serif !important;
        border: none !important;
        width: 100% !important;
