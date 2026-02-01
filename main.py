import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום", layout="centered")

# עיצוב CSS ליישור ימין מוחלט
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'Assistant', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        text-align: right !important;
        display: block !important;
        width: 100% !important;
    }
    div.stButton > button {
        background-color: #E65100 !important;
        color: white !important;
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)

# חיבור לגליון
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# לוגואים
logo2_url = f"https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/{urllib.parse.quote('לוגו חדש (2).png')}"
col1, col2, col3 = st.columns([1, 2, 1])
with col1: st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo1.png", width=80)
with col2: 
    st.markdown("<h2 style='text-align: center; color: #333333;'>נוימן אלומיניום</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #E65100; font-weight: bold;'>ניהול מלאי</p>", unsafe_allow_html=True)
with col3: st.image(logo2_url, width=110)

st.write("---")

# חיפוש
st.markdown("<div style='color: #333333; font-weight: bold;'>🔍 חיפוש פריט</div>", unsafe_allow_html=True)
search_query = st.text_input("הקלידי כאן לחיפוש (שם, מדף או מיקום)", key="search_input_main")

filtered_df = df.copy()
if search_query:
    filtered_df = filtered_df[filtered_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]

# הוספה - שם פריט ללא הגבלה
with st.expander("➕ הוספת פריט חדש", expanded=False):
    with st.form("new_item_form", clear_on_submit=True):
        n_name = st.text_input("שם הפריט (אותיות, מספרים וסימנים)", key="f_name")
        c1, c2, c3 = st.columns(3)
        with c1: n_shelf = st.text_input("מדף", key="f_shelf")
        with c2: n_aisle = st.number_input("מעבר", step=1, format="%d", key="f_aisle")
        with c3: n_floor = st.number_input("קומה", step=1, format="%d", key="f_floor")
        
        if st.form_submit_button("שמור במערכת"):
            if n_name:
                new_row = pd.DataFrame([{"שם פריט": n_name, "מדף": n_shelf, "מעבר": n_aisle, "קומה": n_floor}])
                updated_df = pd.concat([df, new_row], ignore_index=True)
                try:
                    conn.update(data=updated_df)
                    st.success(f"הפריט '{n_name}' נשמר בהצלחה!")
                    st.rerun()
                except Exception as e:
                    st.error("שגיאה בשמירה. ודאי שה-Secrets מוגדרים בדיוק לפי ההוראות.")

st.dataframe(filtered_df, use_container_width=True, hide_index=True)
