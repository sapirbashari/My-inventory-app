import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום - ניהול מלאי", layout="centered")

# הגדרת הצבעים שביקשת
color_orange = "#E65100" # כתום לוגו
color_light_grey = "#F2F2F2" # אפור בהיר לקוביות
color_dark_grey = "#333333" # אפור כהה לטקסט

# עיצוב CSS מותאם אישית (RTL מלא)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Assistant', sans-serif;
        direction: RTL;
        text-align: right;
    }}
    /* קוביות חיפוש באפור בהיר */
    .stTextInput > div > div > input {{
        background-color: {color_light_grey} !important;
        color: {color_dark_grey} !important;
        border-radius: 8px !important;
    }}
    /* כפתור בכתום */
    div.stButton > button {{
        background-color: {color_orange} !important;
        color: white !important;
        border-radius: 8px !important;
        width: 100% !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# טיפול בלוגו השני עם השם המיוחד
logo2_name = urllib.parse.quote("לוגו חדש (2).png")
logo2_url = f"https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/{logo2_
