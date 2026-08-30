from datetime import datetime
import os
import streamlit as st

FILE_PATH = "oikonomika.txt"

st.title("📊 Διαχείριση Οικονομικών")


# Συνάρτηση για φόρτωση δεδομένων
def load_data():
  if not os.path.exists(FILE_PATH):
    return []
  entries = []
  with open(FILE_PATH, "r", encoding="utf-8") as f:
    for line in f:
      parts = line.strip().split(" | ")
      if len(parts) == 4:
        entries.append({
            "id": parts[0],
            "date": parts[1],
            "poso": parts[2],
            "katigoria": parts[3],
            "perigrafi": parts[4] if len(parts) > 4 else "",
        })
  return entries


# Συνάρτηση για αποθήκευση δεδομένων
def save_entry(poso, katigoria, perigrafi):
  entry_id = datetime.now().strftime("%Y%m%d%H%M%S")
  date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
  with open(FILE_PATH, "a", encoding="utf-8") as f:
    f.write(f"{entry_id} | {date_str} | {poso} | {katigoria} | {perigrafi}\n")


# Συνάρτηση για διαγραφή εγγραφής
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
  st.subheader("Προσθήκη Νέας Εγγραφής")
  col1, col2 = st.columns(2)
  with col1:
    poso = st.text_input("Ποσό (€)")
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

  perigrafi = st.text_input("Περιγραφή")
  submit_button = st.form_submit_button(label="💾 Αποθήκευση")

if submit_button:
  if not poso.strip():
    st.warning("Παρακαλώ συμπλήρωσε το ποσό.")
  else:
    try:
      float(poso)
      save_entry(poso, katigoria, perigrafi)
      st.success("Η εγγραφή αποθηκεύτηκε επιτυχώς!")
      st.rerun()
    except ValueError:
      st.error("Το ποσό πρέπει να είναι αριθμός.")

# Εμφάνιση δεδομένων και στατιστικών
st.divider()
st.subheader("Ιστορικό & Στατιστικά")

entries = load_data()

if entries:
  # Υπολογισμός συνολικού ποσού
  total_spent = sum(float(e["poso"]) for e in entries)

  col_m1, col_m2 = st.columns(2)
  col_m1.metric("Συνολικό Ποσό", f"{total_spent:.2f} €")
  col_m2.metric("Συνολικές Εγγραφές", len(entries))

  st.write("---")

  # Λίστα εγγραφών με κουμπί διαγραφής
  for entry in entries:
    c1, c2, c3, c4 = st.columns([2, 2, 4, 1])
    c1.text(entry["date"])
    c2.text(f"{entry['poso']} € ({entry['katigoria']})")
    c3.text(entry["perigrafi"] if entry["perigrafi"] else "-")
    if c4.button("❌", key=f"del_{entry['id']}", help="Διαγραφή εγγραφής"):
      delete_entry(entry["id"])
      st.rerun()
else:
  st.info("Δεν υπάρχουν αποθηκευμένες εγγραφές ακόμα.")
