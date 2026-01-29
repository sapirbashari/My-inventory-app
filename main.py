
import streamlit as st
import pandas as pd

# הגדרות דף
st.set_page_config(page_title="ניהול מלאי", layout="wide")

# תצוגת לוגואים בפינות העליונות
col_logo1, col_title, col_logo2 = st.columns([1, 2, 1])

with col_logo1:
    # לוגו 1 - כתום
    st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo1.png", width=100)

with col_title:
    st.markdown("<h1 style='text-align: center; color: #D35400;'>ניהול מלאי</h1>", unsafe_allow_html=True)

with col_logo2:
    # לוגו 2 - "ירוק"
    st.image("https://raw.githubusercontent.com/sapirbashari/My-inventory-app/main/logo2.png", width=100)

# אתחול בסיס נתונים בזיכרון
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame(columns=['שם פריט', 'מדף', 'מעבר', 'קומה'])

# --- אזור הוספת פריט ---
with st.expander("➕ הוספת פריט חדש", expanded=False):
    with st.form("add_form", clear_on_submit=True):
        name = st.text_input("שם הפריט")
        col1, col2, col3 = st.columns(3)
        shelf = col1.text_input("מדף (אות)")
        aisle = col2.number_input("מעבר (מספר)", min_value=1, step=1)
        floor = col3.number_input("קומה (מספר)", min_value=1, step=1)
        
        if st.form_submit_button("שמור במערכת"):
            new_data = pd.DataFrame([[name, shelf, aisle, floor]], 
                                    columns=['שם פריט', 'מדף', 'מעבר', 'קומה'])
            st.session_state.inventory = pd.concat([st.session_state.inventory, new_data], ignore_index=True)
            st.success(f"הפריט {name} נוסף למיקום: מדף {shelf}, מעבר {aisle}, קומה {floor}")

# --- אזור חיפוש ---
st.write("---")
search_term = st.text_input("🔍 חיפוש מהיר (לפי שם, מדף, מעבר או קומה):")

# סינון הנתונים לפי החיפוש
df = st.session_state.inventory
if search_term:
    mask = df.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
    display_df = df[mask]
else:
    display_df = df

# הצגת הטבלה
st.write("### רשימת מלאי מעודכנת")
st.dataframe(display_df, use_container_width=True)

