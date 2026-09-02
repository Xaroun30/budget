import datetime
import streamlit as st

# Ρύθμιση σελίδας
st.set_page_config(page_title="Διαχείριση Οικονομικών", page_icon="💸")

st.title("💸 Διαχείριση Οικονομικών")

# Αρχικοποίηση session state για την αποθήκευση των εγγραφών
if "transactions" not in st.session_state:
    st.session_state.transactions = []

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

    # Custom CSS για το μπορντό κουμπί αποθήκευσης
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
            is_income = "Έσοδο" in category
            st.session_state.transactions.append({
                "date": datetime.date.today(),
                "category": category,
                "amount": amount,
                "description": description,
                "type": "Έσοδο" if is_income else "Έξοδο",
            })
            st.success("Η καταχώριση αποθηκεύτηκε!")
        else:
            st.warning("Παρακαλώ εισάγετε ποσό μεγαλύτερο του 0.")

st.divider()

# Ενότητα Ιστορικό & Σύνολα
st.header("📊 Ιστορικό & Σύνολα")

total_income = sum(
    t["amount"]
    for t in st.session_state.transactions
    if t["type"] == "Έσοδο"
)
total_expenses = sum(
    t["amount"]
    for t in st.session_state.transactions
    if t["type"] == "Έξοδο"
)

st.subheader("Έσοδα")
st.title(f"{total_income:.2f}€")

st.subheader("Έξοδα")
st.title(f"{total_expenses:.2f}€")
