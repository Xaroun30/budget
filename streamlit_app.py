from datetime import datetime
import os
import streamlit as st

# Ρύθμιση σελίδας
st.set_page_config(
    page_title="Διαχείριση Οικονομικών", page_icon="💳", layout="centered"
)

FILE_PATH = "oikonomika.txt"

# Επαγγελματικό CSS styling (μινιμαλιστικό, καθαρό, χωρίς υπερβολές)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    .entry-card {
        background-color: #ffffff;
        padding: 12px 16px;
        border-radius: 6px;
        margin-bottom: 8px;
        border: 1px solid #e9ecef;
        display: flex;
        align-items: center;
        justify-content: space-between;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💳 Διαχείριση Οικονομικών")
st.write("Παρακολουθήστε τα έξοδά σας με ακρίβεια και καθαρότητα.")


# Συνάρτηση φόρτωσης δεδομένων
def load_data():
  if not os.path.exists(FILE_PATH):
    return []
  entries = []
  with open(FILE_PATH, "r", encoding="utf-8") as f:
    for line in f:
      parts = line.strip().split(" | ")
      if len(parts) >= 4:
        entries.append({
            "id": parts[0],
            "date": parts[1],
            "poso": parts[2],
            "katigoria": parts[3],
            "perigrafi": parts[4] if len(parts) > 4 else "",
        })
  return entries


# Συνάρτηση αποθήκευσης
def save_entry(poso, katigoria, perigrafi):
  entry_id = datetime.now().strftime("%Y%m%d%H%M%S")
  date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
  with open(FILE_PATH, "a", encoding="utf-8") as f:
    f.write(f"{entry_id} | {date_str} | {poso} | {katigoria} | {perigrafi}\n")


# Συνάρτηση διαγραφής
def delete_entry(entry_id):
  entries = load_data()
  with open(FILE_PATH, "w", encoding="utf-8") as f:
    for entry in entries:
      if entry["id"] != entry_id:
        f.write(
            f"{entry['id']} | {entry['date']} | {entry['poso']} |"
            f" {entry['katigoria']} | {entry['perigrafi']}\n"
        )


# Φόρμα εισαγωγής
with st.form("budget_form", clear_on_submit=True):
  st.subheader("➕ Νέα Καταχώρηση")
  col1, col2 = st.columns(2)
  with col1:
    poso = st.text_input("Ποσό (€)", placeholder="π.χ. 25.50")
  with col2:
    katigoria = st.selectbox(
        "Κατηγορία",
        [
            "Σούπερ Μάρκετ",
            "Λογαριασμοί",
            "Ψυχαγωγία",
            "Φαγητό",
            "Διαδίκτυο",
            "Άλλο",
        ],
    )

  perigrafi = st.text_input(
      "Περιγραφή (προαιρετικό)", placeholder="π.χ. Ψώνια εβδομάδας"
  )
  submit_button = st.form_submit_button(
      label="💾 Αποθήκευση Εγγραφής", use_container_width=True
  )

if submit_button:
  if not poso.strip():
    st.warning("Παρακαλώ συμπλήρωσε το ποσό.")
  else:
    try:
      # Αντικατάσταση κόμματος με τελεία αν ο χρήστης βάλει κόμμα
      poso_clean = poso.strip().replace(",", ".")
      float(poso_clean)
      save_entry(poso_clean, katigoria, perigrafi)
      st.success("Η εγγραφή αποθηκεύτηκε επιτυχώς!")
      st.rerun()
    except ValueError:
      st.error("Το ποσό πρέπει να είναι έγκυρος αριθμός.")

# Ανάγνωση δεδομένων για τα στατιστικά και τη λίστα
entries = load_data()

st.divider()

if entries:
  # Υπολογισμοί
  total_spent = sum(float(e["poso"]) for e in entries)
  total_entries = len(entries)

  # Υπολογισμός ανα κατηγορία
  category_totals = {}
  for e in entries:
    cat = e["katigoria"]
    category_totals[cat] = category_totals.get(cat, 0.0) + float(e["poso"])

  # Εμφάνιση βασικών μετρικών
  st.subheader("📊 Στατιστικά Επισκόπηση")
  m1, m2 = st.columns(2)
  m1.metric(label="Συνολικό Ποσό", value=f"{total_spent:.2f} €")
  m2.metric(label="Συνολικές Εγγραφές", value=total_entries)

  # Ανάλυση ανά κατηγορία με μπάρες προόδου
  with st.expander("📈 Ανάλυση ανά Κατηγορία", expanded=True):
    for cat, amount in category_totals.items():
      percentage = amount / total_spent if total_spent > 0 else 0
      col_c1, col_c2, col_c3 = st.columns([2, 4, 2])
      col_c1.write(f"**{cat}**")
      col_c2.progress(percentage)
      col_c3.write(f"**{amount:.2f} €**")

  st.divider()

  # Ιστορικό και διαγραφή
  st.subheader("📋 Ιστορικό Συναλλαγών")

  for entry in reversed(entries):  # Νεότερες πρώτες
    cols = st.columns([2, 2, 4, 1])
    cols[0].text(entry["date"])
    cols[1].text(f"{entry['poso']} €")
    cols[2].text(
        f"[{entry['katigoria']}]"
        + (f" - {entry['perigrafi']}" if entry["perigrafi"] else "")
    )
    if cols[3].button("❌", key=f"del_{entry['id']}", help="Διαγραφή"):
      delete_entry(entry["id"])
      st.rerun()

else:
  st.info(
      "Δεν υπάρχουν αποθηκευμένες εγγραφές ακόμα. Πρόσθεσε την πρώτη σου"
      " καταχώρηση παραπάνω!"
  )
