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

    # Custom CSS για το κουμπί
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
            try:
                # Διαβάζουμε τα υπάρχοντα δεδομένα
                data = conn.read(ttl=0)
                
                # Υπολογισμός τελικού ποσού (+ για έσοδο, - για έξοδο)
                final_amount = amount if "Έσοδο" in category else -amount
                desc_text = f"[{category}] {description}".strip()
                today_str = datetime.date.today().strftime("%Y-%m-%d")
                
                # Δημιουργία νέας εγγραφής
                new_row = {
                    "Ημερομηνία": today_str,
                    "Περιγραφή": desc_text,
                    "Ποσό": final_amount
                }
                
                # Προσθήκη και ενημέρωση
                updated_df = data._append(new_row, ignore_index=True)
                conn.update(data=updated_df)
                
                st.success("Η καταχώριση αποθηκεύτηκε επιτυχώς!")
                st.rerun()
            except Exception as err:
                st.error("Πρόβλημα σύνδεσης. Βεβαιώσου ότι το Google Sheet είναι ρυθμισμένο ως 'Συντάκτης' (Editor) σε όποιον έχει το link.")
        else:
            st.warning("Παρακαλώ εισάγετε ποσό μεγαλύτερο του 0.")

st.divider()

# Ενότητα Ιστορικό & Σύνολα
st.header("📊 Ιστορικό & Σύνολα")

try:
    df = conn.read(ttl=0)
    if not df.empty and "Ποσό" in df.columns:
        # Μετατροπή στήλης Ποσό σε αριθμούς
        df["Ποσό"] = df["Ποσό"].astype(float)
        
        total_income = df[df["Ποσό"] > 0]["Ποσό"].sum()
        total_expenses = abs(df[df["Ποσό"] < 0]["Ποσό"].sum())

        st.subheader("Έσοδα")
        st.title(f"{total_income:.2f}€")

        st.subheader("Έξοδα")
        st.title(f"{total_expenses:.2f}€")
    else:
        st.info("Δεν υπάρχουν ακόμα καταχωρίσεις.")
except Exception:
    st.info("Πρόσθεσε τα Secrets στο Streamlit Cloud για να εμφανιστούν τα σύνολα.")
