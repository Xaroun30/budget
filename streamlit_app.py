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
            final_amount = amount if "Έσοδο" in category else -amount
            desc_text = f"[{category}] {description}".strip()
            today_str = datetime.date.today().strftime("%Y-%m-%d")

            # Αποστολή στη Google Form
            form_data = {
                "entry.1000000": today_str,
                "entry.1000001": desc_text,
                "entry.1000002": str(final_amount),
            }

            try:
                requests.post(FORM_URL, data=form_data)
                st.success("Η καταχώριση αποθηκεύτηκε επιτυχώς!")
                st.rerun()
            except Exception:
                st.error("Σφάλμα κατά την αποστολή των δεδομένων.")
        else:
            st.warning("Παρακαλώ εισάγετε ποσό μεγαλύτερο του 0.")

st.divider()
st.header("📊 Ιστορικό & Σύνολα")

try:
    df = pd.read_csv(SHEET_CSV_URL)
    if not df.empty and len(df.columns) >= 3:
        # Παίρνουμε τη 3η στήλη ως Ποσό
        amount_col = df.columns[2]
        df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce").fillna(0)

        total_income = df[df[amount_col] > 0][amount_col].sum()
        total_expenses = abs(df[df[amount_col] < 0][amount_col].sum())

        st.subheader("Έσοδα")
        st.title(f"{total_income:.2f}€")

        st.subheader("Έξοδα")
        st.title(f"{total_expenses:.2f}€")
    else:
        st.info("Δεν υπάρχουν ακόμα καταχωρίσεις.")
except Exception:
    st.info("Αναμονή για τις πρώτες εγγραφές στο Google Sheet.")
