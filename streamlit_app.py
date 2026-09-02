import datetime
import streamlit as st
from streamlit_gsheets import GSheetsConnection

# Ρύθμιση σελίδας
st.set_page_config(page_title="Διαχείριση Οικονομικών", page_icon="💸")

st.title("💸 Διαχείριση Οικονομικών")

# Σύνδεση με το Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

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

    # Custom CSS για το μπορντό κουμπί
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
            # Διαβάζουμε τα υπάρχοντα δεδομένα από το Google Sheet
            existing_data = conn.read(worksheet="Φύλλο1", ttl=0)
            
            # Δημιουργούμε τη νέα εγγραφή
            new_entry = {
                "Ημερομηνία": datetime.date.today().strftime("%Y-%m-%d"),
                "Περιγραφή": f"[{category}] {description}".strip(),
                "Ποσό": amount if "Έσοδο" in category else -amount
            }
            
            # Προσθέτουμε τη νέα εγγραφή και ενημερώνουμε το Google Sheet
            updated_data = existing_data._append(new_entry, ignore_index=True)
            conn.update(worksheet="Φύλλο1", data=updated_data)
            
            st.success("Η καταχώριση αποθηκεύτηκε στο Google Sheet!")
            st.rerun()
        else:
            st.warning("Παρακαλώ εισάγετε ποσό μεγαλύτερο του 0.")

st.divider()

# Ενότητα Ιστορικό & Σύνολα από το Google Sheet
st.header("📊 Ιστορικό & Σύνολα")

try:
    df = conn.read(worksheet="Φύλλο1", ttl=0)
    
    if not df.empty and "Ποσό" in df.columns:
        # Υπολογισμός Εσόδων και Εξόδων
        total_income = df[df["Ποσό"] > 0]["Ποσό"].sum()
        total_expenses = abs(df[df["Ποσό"] < 0]["Ποσό"].sum())
        
        st.subheader("Έσοδα")
        st.title(f"{total_income:.2f}€")

        st.subheader("Έξοδα")
        st.title(f"{total_expenses:.2f}€")
    else:
        st.info("Δεν υπάρχουν ακόμα καταχωρίσεις.")
except Exception as e:
    st.info("Σύνδεσε τα Secrets του Google Sheet στο Streamlit Cloud για να εμφανιστούν τα σύνολα.")
