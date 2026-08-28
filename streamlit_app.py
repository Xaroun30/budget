import streamlit as st
from datetime import datetime
import os

FILE_PATH = "oikonomika.txt"

st.title("Διαχείριση Οικονομικών")

with st.form("budget_form"):
    poso = st.text_input("Ποσό (€)")
    katigoria = st.selectbox(
        "Κατηγορία",
        ["Σούπερ Μάρκετ", "Λογαριασμοί", "Ψυχαγωγία", "Φαγητό", "Άλλο"],
    )
    perigrafi = st.text_input("Περιγραφή")
    submit_button = st.form_submit_button(label="Αποθήκευση")

if submit_button:
    if not poso.strip():
        st.error("Βάλε ένα ποσό!")
    else:
        try:
            val = float(poso.replace(",", "."))
            date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            teksto = f"[{date_str}] - {katigoria}: {val:.2f}€ ({perigrafi})\n"
            
            with open(FILE_PATH, "a", encoding="utf-8") as f:
                f.write(teksto)
            st.success("Καταχωρήθηκε επιτυχώς!")
        except ValueError:
            st.error("Βάλτε έναν έγκυρο αριθμό για το ποσό!")

st.subheader("Ιστορικό Συναλλαγών")
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    if lines:
        for line in reversed(lines):
            st.write(line.strip())
    else:
        st.info("Δεν υπάρχουν ακόμη καταχωρήσεις.")
else:
    st.info("Δεν βρέθηκε αρχείο δεδομένων.")
