from datetime import datetime
import os
import streamlit as st

# Ορισμός αρχείου αποθήκευσης
FILE_PATH = "oikonomika.txt"

# Επαγγελματικό Design: Σκοτεινό μπλε φόντο και μπορντό κουμπιά με Custom CSS
st.markdown(
    """
    <style>
    /* Σκούρο μπλε φόντο κεντρικής σελίδας */
    .stApp {
        background-color: #0d1b2a;
        color: #e0e1dd;
    }
    
    /* Γενικά κείμενα και τίτλοι */
    h1, h2, h3, h4, h5, h6, label, p, span {
        color: #e0e1dd !important;
    }
    
    /* Μπορντό κουμπιά (Classic Burgundy / Wine) */
    div.stButton > button, div.stFormSubmitButton > button {
        background-color: #722F37 !important;
        color: #ffffff !important;
        border-radius: 8px;
        border: none;
        font-weight: bold;
        width: 100%;
        padding: 0.5rem 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    div.stButton > button:hover, div.stFormSubmitButton > button:hover {
        background-color: #582229 !important;
        color: #ffffff !important;
    }
    
    /* Sidebar σκούρο μπλε */
    [data-testid="stSidebar"] {
        background-color: #1b263b;
        color: #e0e1dd;
    }
    
    /* Κάρτες Metrics */
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💸 Διαχείριση Οικονομικών")

# Γρήγορη Φόρμα Καταχώρησης (Κατηγορία & Ποσό δίπλα-δίπλα)
with st.form("budget_form", clear_on_submit=True):
  col1, col2 = st.columns(2)

  with col1:
    katigoria = st.selectbox(
        "Κατηγορία",
        [
            "Μισθός (Έσοδο)",
            "Market",
            "Βενζίνη",
            "Τσιγάρα",
            "Λογαριασμός",
            "Διαδίκτυο",
            "Διάφορα",
        ],
    )

  with col2:
    poso = st.text_input("Ποσό (€)")

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

        # Έλεγχος αν είναι έσοδο (πιάνει και το παλιό "Έσοδο" και το νέο "Εισόδημα")
        if "Έσοδο" in katigoria_line or "Εισόδημα" in katigoria_line:
          esoda_synolo += ποσο_val
        else:
          eksoda_synolo += ποσο_val
    except Exception:
      pass

  ypoloipo = esoda_synolo - eksoda_synolo

  # Εμφάνιση συνολικών καρτελών (Metrics)
  col_m1, col_m2, col_m3 = st.columns(3)
  col_m1.metric("Έσοδα", f"{esoda_synolo:.2f}€")
  col_m2.metric("Έξοδα", f"{eksoda_synolo:.2f}€")
  col_m3.metric("Υπόλοιπο", f"{ypoloipo:.2f}€")

  st.markdown("---")

  # Εμφάνιση ιστορικού (πιο πρόσφατα πάνω)
  for line in reversed(valid_lines):
    st.text(line.strip())
else:
  st.info("Δεν υπάρχουν ακόμη καταχωρήσεις.")
