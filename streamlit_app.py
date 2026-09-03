import datetime
import pandas as pd
import requests
import streamlit as st

st.set_page_config(page_title="Διαχείριση Οικονομικών", page_icon="💸")
st.title("💸 Διαχείριση Οικονομικών")

# URL υποβολής Google Form
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfiLO2OQRHmMLUDvQPLzkcb7mZecFmCd24qZxzMC4Q7-4bbdw/formResponse"

# URL ανάγνωσης Google Sheet (CSV)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/1dKZXM01_eTYojDcxBZH9G6PlsPel2bwxoVldJ7BmpWg/gviz/tq?tqx=out:csv"

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
        if amount > 0:
            # Θετικό ποσό για έσοδο, αρνητικό για έξοδο
            final_amount = amount if "Έσοδο" in category else -amount

            # Στοιχεία φόρμας με τα σωστά entry IDs
            form_data = {
                "entry.50882045": category,
                "entry.502352790": str(final_amount),
                "entry.1898516613": description,
            }

            try:
                requests.post(FORM_URL, data=form_data)
                st.success(f"Αποθηκεύτηκαν {amount:.2f}€ στην κατηγορία '{category}'!")
                st.rerun()
            except Exception:
                st.error("Σφάλμα κατά την αποθήκευση.")
        else:
            st.warning("Παρακαλώ εισάγετε ποσό μεγαλύτερο του 0.")

st.divider()
st.header("📊 Ιστορικό & Σύνολα")

try:
    df = pd.read_csv(SHEET_CSV_URL)
    if not df.empty and len(df.columns) >= 3:
        # Μετατροπή στήλης ποσού (3η στήλη) σε αριθμό
        amount_col = df.columns[2]
        df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0)

        total_income = df[df[amount_col] > 0][amount_col].sum()
        total_expenses = abs(df[df[amount_col] < 0][amount_col].sum())
        remaining = total_income - total_expenses

        # Εμφάνιση αποτελεσμάτων
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Έσοδα")
            st.title(f"{total_income:.2f}€")
        with col2:
            st.subheader("Έξοδα")
            st.title(f"{total_expenses:.2f}€")

        st.metric(label="💰 Διαθέσιμο Υπόλοιπο (Τι μένει)", value=f"{remaining:.2f}€")

        st.subheader("Πρόσφατες Καταχωρίσεις")
        st.dataframe(df.tail(10), use_container_width=True)
    else:
        st.info("Δεν υπάρχουν ακόμα καταχωρίσεις.")
except Exception:
    st.info("Αναμονή για τις πρώτες εγγραφές στο Google Sheet.")
