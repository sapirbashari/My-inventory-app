import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום", layout="centered")

# צבעים
color_orange = "#E65100" 
color_dark_grey = "#333333" 

# עיצוב CSS - יישור לימין ואייקונים
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="css"], .stApp {{
        font-family: 'Assistant', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }}
    /* פלוס כתום */
    .streamlit-expanderHeader svg {{ fill: {color_orange} !important; }}
    .streamlit-expanderHeader {{ color: {color_orange} !important; font-weight: bold !important; }}
    
    /* כותרות שדות לימין */
    .stTextInput label, .stNumberInput label, .stSelectbox label {{
        text-align: right !important;
        display: block !important;
        width: 100% !important;
    }}

    /* כפתור כתום */
    div.stButton > button {{
        background-color: {color_orange} !important;
        color: white !important;
        width: 100% !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# חיבור לנתונים
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# לוגואים
logo2_url = f"https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/{urllib.parse.quote('לוגו חדש (2).png')}"
col1, col2, col3 = st.columns([1, 2, 1])
with col1: st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo1.png", width=80)
with col2: 
    st.markdown(f"<h2 style='text-align: center; color: {color_dark_grey};'>נוימן אלומיניום</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: {color_orange}; font-weight: bold;'>ניהול מלאי</p>", unsafe_allow_html=True)
with col3: st.image(logo2
