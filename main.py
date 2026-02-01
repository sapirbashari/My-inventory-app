import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום", layout="centered")

# צבעים
color_orange = "#E65100" 
color_dark_grey = "#333333" 

# עיצוב CSS ליישור ימין ואייקונים
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
with col2: st.markdown(f"<h2 style='text-align: center; color: {color_dark_grey};'>נוימן אלומיניום</h2>", unsafe_allow_html=True)
with col3: st.image(logo2_url, width=110)

st.write("---")

# חיפוש חכם (זכוכית מגדלת באפור כהה)
st.markdown(f"<div style='color: {color_dark_grey}; font-weight: bold;'>🔍 חיפוש פריט</div>", unsafe_allow_html=True)
c_s1, c_s2 = st.columns(2)
with c_s1:
    s_name = st.selectbox("שם פריט קיים", ["הכל"] + sorted(df['שם פריט'].unique().tolist()), key="search_select_unique")
with c_s2:
    s_free = st.text_input("חיפוש חופשי (מיקום)", key="search_free_unique")

# סינון
filtered_df = df.copy()
if s_name != "הכל": filtered_df = filtered_df[filtered_df['שם פריט'] == s_name]
if s_free: filtered_df = filtered_df[filtered_df.astype(str).apply(lambda x: x.str.contains(s_free, case=False)).any(axis=1)]

# הוספת פריט
with st.expander("➕ הוספת פריט חדש", expanded=False):
    with st.form("new_add_form", clear_on_submit=True):
        n_name = st.text_input("שם הפריט (אותיות)", key="form_name")
        c1, c2, c3 = st.columns(3)
        with c1: n_shelf = st.text_input("מדף (אותיות)", key="form_shelf")
        with c2: n_aisle = st.number_input("מעבר (מספרים)", step=1, format="%d", key="form_aisle")
        with c3: n_floor = st.number_input("קומה (מספרים)", step=1, format="%d", key="form_floor")
        
        if st.form_submit_button("שמור במערכת"):
            if n_name:
                new_data = pd.DataFrame([{"שם פריט": n_name, "מדף": n_shelf, "מעבר": n_aisle, "קומה": n_floor}])
                updated = pd.concat([df, new_data], ignore_index=True)
                conn.update(data=updated)
                st.success("נשמר!")
                st.rerun()

st.dataframe(filtered_df, use_container_width=True, hide_index=True)
