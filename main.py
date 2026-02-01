import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום", layout="centered")

# צבעים
color_orange = "#E65100" 
color_dark_grey = "#333333" 

# עיצוב CSS - יישור לימין, פונט ואייקונים
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
    
    /* יישור תוויות שדות הקלט */
    .stTextInput label, .stNumberInput label, .stSelectbox label {{
        text-align: right !important;
        display: block !important;
        width: 100% !important;
    }}

    /* כפתור שמירה כתום */
    div.stButton > button {{
        background-color: {color_orange} !important;
        color: white !important;
        width: 100% !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# חיבור לגליון
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# לוגואים - טיפול בשם הקובץ עם סוגריים
logo2_name = "לוגו חדש (2).png"
logo2_url = f"https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/{urllib.parse.quote(logo2_name)}"

col1, col2, col3 = st.columns([1, 2, 1])
with col1: st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo1.png", width=80)
with col2:
    st.markdown(f"<h2 style='text-align: center; color: {color_dark_grey}; margin-bottom: 0;'>נוימן אלומיניום</h2>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align: center; color: {color_orange}; font-weight: bold;'>ניהול מלאי</p>", unsafe_allow_html=True)
with col3: st.image(logo2_url, width=110)

st.write("---")

# --- חיפוש חכם ---
st.markdown(f"<div style='color: {color_dark_grey}; font-weight: bold;'>🔍 חיפוש פריט</div>", unsafe_allow_html=True)
c_s1, c_s2 = st.columns(2)
with c_s1:
    search_name = st.selectbox("בחרי שם פריט", ["הכל"] + sorted(df['שם פריט'].unique().tolist()), key="unique_search_select")
with c_s2:
    search_free = st.text_input("חיפוש חופשי (מדף, מעבר...)", key="unique_search_input")

# פילטור
filtered_df = df.copy()
if search_name != "הכל":
    filtered_df = filtered_df[filtered_df['שם פריט'] == search_name]
if search_free:
    filtered_df = filtered_df[filtered_df.astype(str).apply(lambda x: x.str.contains(search_free, case=False)).any(axis=1)]

# --- טופס הוספה ---
with st.expander("➕ הוספת פריט חדש", expanded=False):
    with st.form("add_new_item_form", clear_on_submit=True):
        new_name = st.text_input("שם הפריט", key="add_field_name")
        c_a, c_b, c_c = st.columns(3)
        with c_a:
            new_shelf = st.text_input("מדף (אותיות)", key="add_field_shelf")
        with c_b:
            new_aisle = st.number_input("מעבר (מספרים)", step=1, format="%d", key="add_field_aisle")
        with c_c:
            new_floor = st.number_input("קומה (מספרים)", step=1, format="%d", key="add_field_floor")
        
        if st.form_submit_button("שמור במערכת"):
            if new_name:
                new_data = pd.DataFrame([{"שם פריט": new_name, "מדף": new_shelf, "מעבר": new_aisle, "קומה": new_floor}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                try:
                    conn.update(data=updated_df)
                    st.success("הפריט נשמר!")
                    st.rerun()
                except Exception:
                    st.error("שגיאת הרשאה: ודאי שהגליון מוגדר כ-Editor ב-Secrets.")

# הצגת הטבלה
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
