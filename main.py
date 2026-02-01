import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# הגדרות דף ועיצוב
st.set_page_config(page_title="ניהול מלאי", layout="wide")

# תצוגת לוגואים בפינות (כפי שביקשת בעיצוב)
col_l, col_m, col_r = st.columns([1, 2, 1])
with col_l:
    st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo1.png", width=120)
with col_m:
    st.markdown("<h1 style='text-align: center; color: #4A2B1F;'>ניהול מלאי</h1>", unsafe_allow_html=True)
with col_r:
    st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo2.png", width=120)

# חיבור ל-Google Sheets (סנכרון נתונים בזמן אמת)
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# --- אזור חיפוש (מופיע למעלה לפי העיצוב) ---
st.write("### חיפוש פריט")
search_query = st.text_input("הקלד שם פריט, מדף, מעבר או קומה:", placeholder="חיפוש...")

# --- אזור הוספת פריט ---
with st.container():
    st.write("---")
    st.write("### הוספת פריט חדש")
    c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
    new_name = c1.text_input("שם פריט")
    new_shelf = c2.text_input("מדף (A-Z)")
    new_aisle = c3.text_input("מעבר (מספר)")
    new_floor = c4.text_input("קומה (מספר)")
    
    if st.button("Commit changes (שמור)"):
        if new_name:
            new_row = pd.DataFrame([{"שם פריט": new_name, "מדף": new_shelf, "מעבר": new_aisle, "קומה": new_floor}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("הנתונים נשמרו וסונכרנו!")
            st.rerun()

# סינון נתונים והצגה
if search_query:
    df = df[df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)]

st.write("---")
st.write("### רשימת המלאי")
st.dataframe(df, use_container_width=True, hide_index=True)
