import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום", layout="centered")

# הגדרת צבעים
color_orange = "#E65100" # הכתום של הלוגו
color_light_grey = "#F2F2F2" 
color_dark_grey = "#333333" 

# עיצוב CSS - פונט Assistant וצבעים
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    
    /* שינוי פונט לכל האפליקציה ויישור לימין */
    html, body, [class*="css"], .stApp {{
        font-family: 'Assistant', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }}
    
    /* צביעת כותרת ה-Expander (הפלוס והטקסט) בכתום */
    .streamlit-expanderHeader {{
        color: {color_orange} !important;
        font-weight: bold !important;
