from datetime import datetime
import os
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# Σύνδεση με το Google Sheet
conn = st.connection("gsheets", type=GSheetsConnection)

# Σκούρο μπλε φόντο & Design
st.markdown(
    """
    <style>
    .stApp {
        background-color: #0d1b2a;
        color: #e0e1dd;
    }
    h1, h2, h3, h4, h5, h6, label {
        color: #e0e1dd !important;
    }
    .stButton>button {
        background-color: #1b263b;
        color: #e0e1dd;
        border: 1px solid #415a77;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("💰 Οικονομικός Διαχειριστής")

# Ανάγνωση δεδομένων από το Google Sheet
try:
    data = conn.read(ttl=0)
except Exception:
    data = pd.DataFrame(columns=["Ημερομηνία", "Περιγραφή", "Ποσό", "Τύπος"])

# Φόρμα εισαγωγής
with st.form("add_transaction"):
    date = st.date_input("Ημερομηνία", value=datetime.now())
    description = st.text_input("Περιγραφή")
    amount = st.number_input("Ποσό (€)", min_value=0.0, format="%.2f")
    trans_type = st.selectbox("Τύπος", ["Έσοδο", "Έξοδο"])
    submitted = st.form_submit_button("Αποθήκευση")

    if submitted:
        if description.strip() == "":
            st.warning("Παρακαλώ συμπλήρωσε περιγραφή.")
        else:
            new_row = pd.DataFrame([{
                "Ημερομηνία": str(date),
                "Περιγραφή": description,
                "Ποσό": amount,
                "Τύπος": trans_type
            }])
            
            # Προσθήκη νέας εγγραφής
            updated_df = pd.concat([data, new_row], ignore_index=True)
            
            # Αποθήκευση στο Google Sheet
            conn.update(data=updated_df)
            st.success("Η καταχώρηση αποθηκεύτηκε μόνιμα στο Google Sheet!")
            st.rerun()

# Εμφάνιση ιστορικού
st.subheader("📊 Ιστορικό Καταχωρίσεων")
st.dataframe(data, use_container_width=True)
