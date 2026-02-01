import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# הגדרות דף
st.set_page_config(page_title="ניהול מלאי", layout="centered")

# לוגואים בפינות (logo1.png ו-logo2.png ב-GitHub)
col_l, col_r = st.columns([1, 1])
with col_l:
    st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo1.png", width=100)
with col_r:
    st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo2.png", width=120)

st.markdown("<h2 style='text-align: center;'>ניהול מלאי</h2>", unsafe_allow_html=True)

# חיבור לגוגל שיטס
conn = st.connection("gsheets", type=GSheetsConnection)

# קריאת נתונים עם מנגנון הגנה משגיאות
try:
    df = conn.read()
except Exception as e:
    st.error("מתחבר לבסיס הנתונים... וודאי שהקישור ב-Secrets תקין והטבלה פתוחה לצפייה.")
    df = pd.DataFrame(columns=['שם פריט', 'מדף', 'מעבר', 'קומה'])

# חיפוש למעלה
search = st.text_input("🔍 חיפוש לפי שם פריט או מיקום:")

# הוספת פריט (לפי הסדר שביקשת)
with st.expander("➕ הוספת פריט חדש"):
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("שם פריט")
        c1, c2, c3 = st.columns(3)
        shelf = c1.text_input("מדף (אות)")
        aisle = c2.text_input("מעבר (מספר)")
        floor = c3.text_input("קומה (מספר)")
        
        if st.form_submit_button("שמור שינויים"):
            new_row = pd.DataFrame([{"שם פריט": name, "מדף": shelf, "מעבר": aisle, "קומה": floor}])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("נשמר בהצלחה!")
            st.rerun()

# הצגת הטבלה
if search:
    df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

st.write("---")
st.dataframe(df, use_container_width=True, hide_index=True)
