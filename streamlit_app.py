from datetime import datetime
import os
import streamlit as st

# Ρύθμιση σελίδας
st.set_page_config(
    page_title="Διαχείριση Οικονομικών", page_icon="💳", layout="centered"
)

FILE_PATH = "oikonomika.txt"

# Μινιμαλιστικό και καθαρό CSS styling
st.markdown("""
    <style>
    .stMetric {
        background-color: #ffffff;
        padding: 12px;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
    }
    </style>
""", unsafe_allow_html=True)

st.title("💳 Διαχείριση Οικονομικών")
st.write(
    "Όλα τα δεδομένα, τα στατιστικά και η διαχείριση σε μία ενιαία σελίδα."
)


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


# Φόρμα εισαγωγής με κουμπιά δίπλα-δίπλα (Αποθήκευση & Διαγραφή τελευταίου)
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

  # Κουμπιά δίπλα-δύπλα στη φόρμα
  f_col1, f_col2 = st.columns(2)
  with f_col1:
    submit_button = st.form_submit_button(
        label="💾 Αποθήκευση", use_container_width=True
    )
  with f_col2:
    # Ενημερωτικό μήνυμα δίπλα στο κουμπί αποθήκευσης
    st.markdown(
        "<div style='text-align: center; color: #6c757d; font-size: 12px; "
        "margin-top: 10px;'>💡 Η διαγραφή γίνεται κάτω στο ιστορικό</div>",
        unsafe_allow_html=True,
    )

if submit_button:
  if not poso.strip():
    st.warning("Παρακαλώ συμπλήρωσε το ποσό.")
  else:
    try:
      poso_clean = poso.strip().replace(",", ".")
      float(poso_clean)
      save_entry(poso_clean, katigoria, perigrafi)
      st.success("Η εγγραφή αποθηκεύτηκε επιτυχώς!")
      st.rerun()
    except ValueError:
      st.error("Το ποσό πρέπει να είναι έγκυρος αριθμός.")

# Ανάγνωση δεδομένων
entries = load_data()

st.divider()

# Εμφάνιση Στατιστικών απευθείας στην οθόνη (χωρίς κρυφά μενού)
st.subheader("📊 Στατιστικά & Ανάλυση")

if entries:
  total_spent = sum(float(e["poso"]) for e in entries)
  total_entries = len(entries)

  # Υπολογισμός ανά κατηγορία
  category_totals = {}
  for e in entries:
    cat = e["katigoria"]
    category_totals[cat] = category_totals.get(cat, 0.0) + float(e["poso"])

  # Βασικές μετρικές
  m1, m2 = st.columns(2)
  m1.metric(label="Συνολικό Ποσό", value=f"{total_spent:.2f} €")
  m2.metric(label="Συνολικές Εγγραφές", value=total_entries)

  st.write("##### 📌 Πού ξοδεύουμε τα περισσότερα (Ανά Κατηγορία):")
  for cat, amount in sorted(
      category_totals.items(), key=lambda x: x[1], reverse=True
  ):
    percentage = (amount / total_spent) * 100 if total_spent > 0 else 0
    c_cat, c_bar, c_val = st.columns([2, 4, 2])
    c_cat.write(f"**{cat}**")
    c_bar.progress(percentage / 100.0)
    c_val.write(f"**{amount:.2f} €** ({percentage:.1f}%)")

  st.divider()

  # Ιστορικό Συναλλαγών με κουμπί διαγραφής δίπλα σε κάθε εγγραφή
  st.subheader("📋 Ιστορικό Συναλλαγών & Διαγραφή")
  st.write("Εδώ μπορείτε να δείτε αναλυτικά τις εγγραφές και να διαγράψετε όποια θέλετε.")

  for entry in reversed(entries):  # Νεότερες πρώτες
    cols = st.columns([2, 2, 4, 1])
    cols[0].text(entry["date"])
    cols[1].text(f"{entry['poso']} €")
    cols[2].text(
        f"[{entry['katigoria']}]"
        + (f" - {entry['perigrafi']}" if entry["perigrafi"] else "")
    )
    if cols[3].button("❌ Διαγ.", key=f"del_{entry['id']}", help="Διαγραφή"):
      delete_entry(entry["id"])
      st.rerun()

else:
  st.info(
      "Δεν υπάρχουν αποθηκευμένες εγγραφές ακόμα. Πρόσθεσε την πρώτη σου"
      " καταχώρηση παραπάνω!"
  )
