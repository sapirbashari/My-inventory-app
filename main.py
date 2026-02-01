import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום", layout="centered")

# צבעים מוגדרים מראש
color_orange = "#E65100" 
color_dark_grey = "#333333" 
color_light_grey = "#F2F2F2" 

# עיצוב CSS - יישור לימין, פונט Assistant וצבעי אייקונים
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    
    /* הגדרות פונט ויישור לימין לכל האפליקציה */
    html, body, [class*="css"], .stApp {{
        font-family: 'Assistant', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }}

    /* יישור כותרות השדות (Labels) לימין */
    label, .stMarkdown p {{
        text-align: right !important;
        display: block !important;
        width: 100% !important;
    }}

    /* צביעת הפלוס בכתום */
    .streamlit-expanderHeader {{
        color: {color_orange} !important;
        fill: {color_orange} !important;
        font-weight: bold !important;
    }}

    /* צביעת הזכוכית מגדלת באפור כהה */
    .stTextInput div[data-baseweb="input"]::before {{
        color: {color_dark_grey} !important;
    }}

    /* עיצוב כפתור שמירה כתום */
    div.stButton > button {{
        background-color: {color_orange} !important;
        color: white !important;
        border: none !important;
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

# חיבור לגוגל שיטס
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

st.write("---")

# --- חלק החיפוש המתקדם ---
st.markdown(f"<div style='color: {color_dark_grey}; font-weight: bold;'>🔍 חיפוש פריט במחסן</div>", unsafe_allow_html=True)

# בחירה מתוך רשימה קיימת או חיפוש חופשי
col_s1, col_s2 = st.columns(2)
with col_s1:
    filter_name = st.selectbox("בחרי שם פריט קיים", ["הכל"] + sorted(df['שם פריט'].unique().tolist()))
with col_s2:
    filter_loc = st.text_input("חיפוש חופשי (מדף, מעבר, קומה)")

# סינון הנתונים
filtered_df = df.copy()
if filter_name != "הכל":
    filtered_df = filtered_df[filtered_df['שם פריט'] == filter_name]
if filter_loc:
    filtered_df = filtered_df[filtered_df.astype(str).apply(lambda x: x.str.contains(filter_loc, case=False)).any(axis=1)]

# --- חלק הוספת פריט ---
with st.expander("➕ הוספת פריט חדש", expanded=False):
    with st.form("add_form", clear_on_submit=True):
        st.markdown("<div style='text-align: right;'><b>שם הפריט</b></div>", unsafe_allow_html=True)
        new_name = st.text_input("", placeholder="הזיני שם פריט...", label_visibility="collapsed")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown("<b>מדף (אות)</b>", unsafe_allow_html=True)
            new_shelf = st.text_input("", placeholder="למשל: A", label_visibility="collapsed")
        with c2:
            st.markdown("<b>מעבר (מספר)</b>", unsafe_allow_html=True)
            new_aisle = st.number_input("", step=1, format="%d", label_visibility="collapsed")
        with c3:
            st.markdown("<b>קומה (מספר)</b>", unsafe_allow_html=True)
            new_floor = st.number_input("", step=1, format="%d", label_visibility="collapsed")
        
        if st.form_submit_button("שמור במערכת"):
            if new_name:
                new_row = pd.DataFrame([{"שם פריט": new_name, "מדף": new_shelf, "מעבר": new_aisle, "קומה": new_floor}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                try:
                    conn.update(data=updated_df)
                    st.success("הפריט נשמר בהצלחה!")
                    st.rerun()
                except Exception as e:
                    st.error("שגיאת הרשאה: ודאי שהגדרת את הגליון כ-Editor ב-Streamlit Secrets.")
            else:
                st.warning("חובה להזין שם פריט")

# הצגת הטבלה המסוננת
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
