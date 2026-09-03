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
    # Ανάγνωση δεδομένων από το Google Sheet
    df = pd.read_csv(SHEET_CSV_URL)

    if not df.empty:
        # Καθαρισμός και ονομασία στηλών
        df = df.iloc[:, :4]  # Κρατάμε τις 4 πρώτες στήλες
        df.columns = ["Ημερομηνία", "Κατηγορία", "Ποσό", "Περιγραφή"]

        # Μετατροπή στήλης Ποσού σε αριθμό
        df["Ποσό"] = pd.to_numeric(df["Ποσό"], errors="coerce")

        # Φιλτράρουμε μόνο τις γραμμές που έχουν πραγματικό ποσό
        valid_df = df.dropna(subset=["Ποσό"]).copy()

        if not valid_df.empty:
            total_income = valid_df[valid_df["Ποσό"] > 0]["Ποσό"].sum()
            total_expenses = abs(valid_df[valid_df["Ποσό"] < 0]["Ποσό"].sum())
            remaining = total_income - total_expenses

            # Εμφάνιση υπολοίπων
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Έσοδα")
                st.title(f"{total_income:.2f}€")
            with col2:
                st.subheader("Έξοδα")
                st.title(f"{total_expenses:.2f}€")

            st.metric(label="💰 Διαθέσιμο Υπόλοιπο (Τι μένει)", value=f"{remaining:.2f}€")

            # Εμφάνιση Αναλυτικού Ιστορικού
            st.subheader("📜 Αναλυτικό Ιστορικό Καταχωρίσεων")
            # Αντιστροφή για να φαίνονται πρώτες οι πιο πρόσφατες
            st.dataframe(valid_df.iloc[::-1], use_container_width=True)
        else:
            st.info("Κάνε την πρώτη σου καταχώριση για να εμφανιστεί το ιστορικό!")
    else:
        st.info("Δεν υπάρχουν ακόμα καταχωρίσεις.")
except Exception:
    st.info("Ανανέωσε τη σελίδα σε λίγο για να φορτώσουν τα δεδομένα.")
