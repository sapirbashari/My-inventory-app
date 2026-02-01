import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום", layout="centered")

# הגדרת צבעים
color_orange = "#E65100" 
color_dark_grey = "#333333" # אפור כהה לזכוכית מגדלת וטקסט
color_light_grey = "#F2F2F2" 

# עיצוב CSS - פונט Assistant, יישור לימין מוחלט וצבעים
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    
    /* יישור כללי מוחלט לימין */
    html, body, [class*="css"], .stApp {{
        font-family: 'Assistant', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }}

    /* דחיפת שדות הקלט והחיפוש לימין */
    .stTextInput, .stExpander, .stDataFrame {{
        direction: RTL !important;
        text-align: right !important;
    }}

    /* צביעת הפלוס והטקסט ב-Expander בכתום */
    .streamlit-expanderHeader {{
        color: {color_orange} !important;
        fill: {color_orange} !important;
        font-weight: bold !important;
    }}

    /* עיצוב שדות החיפוש והזנת נתונים */
    input {{
        background-color: {color_light_grey} !important;
        color: {color_dark_grey} !important;
        text-align: right !important;
        border-radius: 8px !important;
    }}

    /* כפתור שמירה כתום */
    div.stButton > button {{
        background-color: {color_orange} !important;
        color: white !important;
        border: none !important;
        font-weight: bold !important;
        width: 100% !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# טיפול בלוגואים
logo2_name = urllib.parse.quote("לוגו חדש (2).png")
logo2_url = f"https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/{logo2_name}"

col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo1.png", width=80)
with col2:
    st.markdown(f"<h2 style='text-align: center; color: {color_dark_grey};'>נוימן אלומיניום</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: {color_orange}; font-weight: bold;'>ניהול מלאי</p>", unsafe_allow_html=True)
with col3:
    st.image(logo2_url, width=110)

# חיבור לנתונים
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

st.write("---")

# שורת חיפוש - זכוכית מגדלת באפור כהה ויישור לימין
st.markdown(f"<div style='text-align: right;'><b style='color: {color_dark_grey};'>🔍 חיפוש פריט במחסן</b></div>", unsafe_allow_html=True)
search = st.text_input("", placeholder="הקלידי כאן לחיפוש...", label_visibility="collapsed")

# טופס הוספה - פלוס כתום
with st.expander("➕ הוספת פריט חדש", expanded=False):
    with st.form("add_form", clear_on_submit=True):
        st.markdown("<b>שם הפריט</b>", unsafe_allow_html=True)
        name = st.text_input("", label_visibility="collapsed")
        
        c1, c2, c3 = st.columns(3)
        with c1: 
            st.markdown("<b>מדף</b>", unsafe_allow_html=True)
            shelf = st.text_input("מדף", label_visibility="collapsed")
        with c2: 
            st.markdown("<b>מעבר</b>", unsafe_allow_html=True)
            aisle = st.text_input("מעבר", label_visibility="collapsed")
        with c3: 
            st.markdown("<b>קומה</b>", unsafe_allow_html=True)
            floor = st.text_input("קומה", label_visibility="collapsed")
        
        if st.form_submit_button("שמור במערכת"):
            if name:
                new_row = pd.DataFrame([{"שם פריט": name, "מדף": shelf, "מעבר": aisle, "קומה": floor}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.success("נשמר בהצלחה!")
                st.rerun()

# הצגת הטבלה
if search:
    df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

st.dataframe(df, use_container_width=True, hide_index=True)
