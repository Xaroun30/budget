from datetime import datetime
import os
import streamlit as st

# Ορισμός διαδρομής για το αρχείο κειμένου
BASE_DIR = os.path.dirname(os.path.abspath(_file_))
FILE_PATH = os.path.join(BASE_DIR, "oikonomika.txt")

st.title("💶 Κοινόχρηστα Οικονομικά")
st.write(
    "Καταχωρήστε τα έσοδα/έξοδά σας για να τα βλέπετε και οι δύο σε πραγματικό"
    " χρόνο."
)

# Φόρμα καταχώρησης
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

        with open(FILE_PATH, "a", encoding="utf-8")