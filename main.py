import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום - ניהול מלאי", layout="centered")

# הגדרת הצבעים שביקשת
color_orange = "#E65100" # כתום כמו הלוגו
color_light_grey = "#F2F2F2" # אפור בהיר לקוביות
color_dark_grey = "#333333" # אפור כהה לכתב

# עיצוב CSS (RTL מלא)
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@400;700&display=swap');
    html, body, [class*="css"] {{ font-family: 'Assistant', sans-serif; direction: RTL; text-align: right; }}
    .stTextInput > div > div > input {{ background-color: {color_light_grey} !important; color: {color_dark_grey} !important; border-radius: 8px; }}
    div.stButton > button {{ background-color: {color_orange} !important; color: white !important; border-radius: 8px; width: 100%; font-weight: bold; border: none; }}
    </style>
    """, unsafe_allow_html=True)

# יצירת הקישור ללוגו השני (עם השם המדויק מהתמונה שלך)
logo2_raw_name = "לוגו חדש (2).png"
logo2_encoded = urllib.parse.quote(logo2_raw_name)
logo2_url = f"https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/{logo2_encoded}"

# כותרת ולוגואים
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo1.png", width=80)
with col2:
    st.markdown(f"<h2 style='text-align: center; color: {color_dark_grey};'>נוימן אלומיניום</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: {color_orange}; font-weight: bold; margin-top: -15px;'>ניהול מלאי</p>", unsafe_allow_html=True)
with col3:
    st.image(logo2_url, width=110)

# חיבור לנתונים
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

st.write("---")

# חיפוש (אפור בהיר עם כתב כהה)
st.markdown(f"<b style='color: {color_orange};'>🔍</b> <b>חיפוש פריט במחסן</b>", unsafe_allow_html=True)
search = st.text_input("", placeholder="הזיני שם פריט, מדף או קומה...", label_visibility="collapsed")

# טופס הוספה
with st.expander("➕ הוספת פריט חדש"):
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("שם הפריט")
        c1, c2, c3 = st.columns(3)
        shelf = c1.text_input("מדף")
        aisle = c2.text_input("מעבר")
        floor = c3.text_input("קומה")
        
        if st.form_submit_button("שמור במערכת"):
            if name:
                new_row = pd.DataFrame([{"שם פריט": name, "מדף": shelf, "מעבר": aisle, "קומה": floor}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                conn.update(data=updated_df)
                st.success("נשמר בהצלחה!")
                st.rerun()

# הצגה
if search:
    df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

st.dataframe(df, use_container_width=True, hide_index=True)
