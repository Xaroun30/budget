import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Διαχείριση Οικονομικών", page_icon="💸")
st.title("💸 Διαχείριση Οικονομικών")

SHEET_URL = "https://docs.google.com/spreadsheets/d/1dKZXM01_eTYojDcxBZH9G6PlsPel2bwxoVldJ7BmpWg/gviz/tq?tqx=out:csv"

# Φόρμα καταχώρισης
with st.container():
    category = st.selectbox(
        "Κατηγορία",
        [
            "Μισθός (Έσοδο)",
            "Άλλο Έσοδο",
            "Φαγητό / Καφέ (Έξοδο)",
            "Λογαριασμοί (Έξοδο)",
            "Αγορές (Έξοδο)",
            "Μεταφορές (Έξοδο)",
        ],
    )
    amount = st.number_input("Ποσό (€)", min_value=0.0, step=0.01, format="%.2f")
    description = st.text_input("Περιγραφή (προαιρετικά)")

    st.markdown(
        """
        <style>
        div.stButton > button:first-child {
            background-color: #722F37;
            color: white;
            border-radius: 5px;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    if st.button("💾 Αποθήκευση"):
        st.info(
            "Για άμεση εγγραφή χωρίς σφάλματα δικαιωμάτων, συνιστάται η χρήση βάσης SQLite ή Google Form Endpoint."
        )

st.divider()
st.header("📊 Ιστορικό & Σύνολα")

try:
    df = pd.read_csv(SHEET_URL)
    if not df.empty and "Ποσό" in df.columns:
        df["Ποσό"] = pd.to_numeric(df["Ποσό"], errors="coerce").fillna(0)
        total_income = df[df["Ποσό"] > 0]["Ποσό"].sum()
        total_expenses = abs(df[df["Ποσό"] < 0]["Ποσό"].sum())

        st.subheader("Έσοδα")
        st.title(f"{total_income:.2f}€")

        st.subheader("Έξοδα")
        st.title(f"{total_expenses:.2f}€")
    else:
        st.info("Δεν βρέθηκαν καταχωρίσεις στο Google Sheet.")
except Exception as e:
    st.error("Δεν ήταν δυνατή η ανάγνωση του Google Sheet.")
