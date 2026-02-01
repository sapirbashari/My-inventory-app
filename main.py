import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
import urllib.parse

# הגדרות דף
st.set_page_config(page_title="נוימן אלומיניום", layout="centered")

# עיצוב CSS - פונט Assistant, יישור לימין וצבעים
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;700&display=swap');
    html, body, [class*="css"], .stApp {
        font-family: 'Assistant', sans-serif !important;
        direction: RTL !important;
        text-align: right !important;
    }
    /* יישור תוויות השדות לימין */
    .stTextInput label, .stNumberInput label, .stSelectbox label {
        text-align: right !important;
        display: block !important;
        width: 100% !important;
    }
    /* כפתור כתום */
    div.stButton > button {
        background-color: #E65100 !important;
        color: white !important;
        width: 100% !important;
        border: none !important;
        height: 3em !important;
        font-weight: bold !important;
    }
    /* פלוס כתום ב-Expander */
    .streamlit-expanderHeader { color: #E65100 !important; }
    .streamlit-expanderHeader svg { fill: #E65100 !important; }
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
    st.markdown("<h2 style='text-align: center; color: #333333; margin-bottom:0;'>נוימן אלומיניום</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #E65100; font-weight: bold;'>ניהול מלאי</p>", unsafe_allow_html=True)
with col3: st.image(logo2_url, width=110)

st.write("---")

# --- חיפוש ---
st.markdown("<div style='color: #333333; font-weight: bold;'>🔍 חיפוש פריט (לפי שם או מיקום)</div>", unsafe_allow_html=True)
c_s1, c_s2 = st.columns(2)
with c_s1:
    search_name = st.selectbox("בחרי פריט מהרשימה", ["הכל"] + sorted(df['שם פריט'].astype(str).unique().tolist()), key="sel_search")
with c_s2:
    search_free = st.text_input("או הקלידי חיפוש חופשי", placeholder="מדף, מעבר...", key="txt_search")

# סינון
filtered_df = df.copy()
if search_name != "הכל":
    filtered_df = filtered_df[filtered_df['שם פריט'] == search_name]
if search_free:
    filtered_df = filtered_df[filtered_df.astype(str).apply(lambda x: x.str.contains(search_free, case=False)).any(axis=1)]

# --- הוספת פריט ---
with st.expander("➕ הוספת פריט חדש למלאי", expanded=False):
    with st.form("add_item_form_v4", clear_on_submit=True):
        # שדה שם פריט - פתוח להכל (אותיות, מספרים, סימנים)
        n_name = st.text_input("שם הפריט (למשל: פרופיל 9000 #2)", key="new_name_val")
        
        c1, c2, c3 = st.columns(3)
        with c1: n_shelf = st.text_input("מדף", key="new_shelf_val")
        with c2: n_aisle = st.number_input("מעבר (מספר)", step=1, format="%d", key="new_aisle_val")
        with c3: n_floor = st.number_input("קומה (מספר)", step=1, format="%d", key="new_floor_val")
        
        if st.form_submit_button("שמור במערכת"):
            if n_name:
                new_data = pd.DataFrame([{"שם פריט": n_name, "מדף": n_shelf, "מעבר": n_aisle, "קומה": n_floor}])
                updated_df = pd.concat([df, new_data], ignore_index=True)
                try:
                    conn.update(data=updated_df)
                    st.success(f"הפריט '{n_name}' נשמר בהצלחה!")
                    st.rerun()
                except Exception:
                    st.error("שגיאת הרשאה: ודאי שהגדרת את הגליון כ-Editor ב-Secrets (type = 'lib').")
            else:
                st.warning("בבקשה הזיני שם פריט")

# הצגת הטבלה
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
