from datetime import datetime
import os
import streamlit as st

# Ορισμός αρχείου αποθήκευσης
FILE_PATH = "oikonomika.txt"

st.title("💸 Διαχείριση Οικονομικών")

# Φόρμα καταχώρησης με καθαρισμό μετά την υποβολή
with st.form("budget_form", clear_on_submit=True):
  poso = st.text_input("Ποσό (€)")
  katigoria = st.selectbox(
      "Κατηγορία",
      [
          "Μισθός (Έσοδο)",
          "Μάρκετ",
          "Βενζίνη",
          "Τσιγάρα",
          "Λογαριασμοί",
          "Διαδίκτυο",
          "Διάφορα",
      ],
  )
  perigrafi = st.text_input("Περιγραφή (προαιρετικά)")

  submit_button = st.form_submit_button(label="💾 Αποθήκευση")

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
      st.rerun()
    except ValueError:
      st.error("Βάλτε έναν έγκυρο αριθμό για το ποσό!")

# Πλαϊνό μενού για Διαχείριση / Διαγραφή
st.sidebar.header("⚙️ Επιλογές Διαχείρισης")
if os.path.exists(FILE_PATH):
  with open(FILE_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()
  valid_lines = [
      line for line in lines if line.strip() and not line.startswith("=")
  ]

  if valid_lines:
    if st.sidebar.button("🗑️ Διαγραφή Τελευταίας Εγγραφής"):
      valid_lines.pop()
      with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.writelines(valid_lines)
      st.sidebar.success("Η τελευταία εγγραφή διαγράφηκε!")
      st.rerun()

    if st.sidebar.button("⚠️ Διαγραφή Ολόκληρου του Ιστορικού"):
      if os.path.exists(FILE_PATH):
        os.remove(FILE_PATH)
      st.sidebar.success("Το ιστορικό καθάρισε!")
      st.rerun()
  else:
    st.sidebar.info("Δεν υπάρχουν εγγραφές για διαγραφή.")
else:
  st.sidebar.info("Δεν βρέθηκε αρχείο δεδομένων.")

# Υπολογισμός και Εμφάνιση Ιστορικού & Συνόλων
st.subheader("📊 Ιστορικό & Σύνολα")

esoda_synolo = 0.0
eksoda_synolo = 0.0
lines = []

if os.path.exists(FILE_PATH):
  with open(FILE_PATH, "r", encoding="utf-8") as f:
    lines = f.readlines()

valid_lines = [
    line for line in lines if line.strip() and not line.startswith("=")
]

if valid_lines:
  for line in valid_lines:
    try:
      parts = line.split(" - ")
      if len(parts) >= 2:
        kat_poso = parts[1].split(": ")
        katigoria_line = kat_poso[0]
        ποσο_str = kat_poso[1].split("€")[0].strip()
        ποσο_val = float(ποσο_str)

        if "Έσοδο" in katigoria_line:
          esoda_synolo += ποσο_val
        else:
          eksoda_synolo += ποσο_val
    except Exception:
      pass

  ypoloipo = esoda_synolo - eksoda_synolo

  # Εμφάνιση συνολικών καρτελών (Metrics)
  col1, col2, col3 = st.columns(3)
  col1.metric("Έσοδα", f"{esoda_synolo:.2f}€")
  col2.metric("Έξοδα", f"{eksoda_synolo:.2f}€")
  col3.metric("Υπόλοιπο", f"{ypoloipo:.2f}€")

  st.markdown("---")

  # Εμφάνιση ιστορικού (πιο πρόσφατα πάνω)
  for line in reversed(valid_lines):
    st.text(line.strip())
else:
  st.info("Δεν υπάρχουν ακόμη καταχωρήσεις.")
