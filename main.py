import streamlit as st
import pandas as pd

# הגדרות עיצוב בסיסיות
st.set_page_config(page_title="ירוק - ניהול מלאי", layout="centered")

# כותרת ולוגו
st.markdown("<h1 style='text-align: center; color: #D35400;'>ירוק - ניהול מלאי</h1>", unsafe_allow_html=True)
st.write("ניהול פריטים ומיקומים בקלות")

# יצירת טבלה לדוגמה (בשלב הבא נחבר לזה בסיס נתונים קבוע)
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['שם פריט', 'כמות', 'מיקום'])

# טופס הוספה
with st.form("add_item"):
    col1, col2, col3 = st.columns(3)
    item_name = col1.text_input("שם פריט")
    quantity = col2.number_input("כמות", min_value=0)
    location = col3.text_input("מיקום")
    submit = st.form_submit_button("הוסף למלאי")
    
    if submit:
        new_row = pd.DataFrame({'שם פריט': [item_name], 'כמות': [quantity], 'מיקום': [location]})
        st.session_state.inventory = pd.concat([st.session_state.inventory, new_row], ignore_index=True)
        st.success("הפריט נוסף בהצלחה!")

# הצגת המלאי
st.write("### המלאי הנוכחי")
st.table(st.session_state.inventory)
