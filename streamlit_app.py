class BudgetTracker:
    def __init__(self):
        self.transactions = []

    def add_transaction(self, category, amount, transaction_type):
        """
        Προσθήκη συναλλαγής.
        transaction_type: 'Income' (Εισόδημα) ή 'Expense' (Έξοδος)
        """
        transaction = {
            "category": category,
            "amount": amount,
            "type": transaction_type
        }
        self.transactions.append(transaction)
        print( επιτυχία: Προστέθηκε {amount}€ στην κατηγορία '{category}' )

    def get_balance(self):
        """Υπολογισμός συνολικού υπολοίπου (Εσόδα - Έξοδα)"""
        total_income = sum(t["amount"] for t in self.transactions if t["type"] == "Income")
        total_expense = sum(t["amount"] for t in self.transactions if t["type"] == "Expense")
        return total_income - total_expense

    def show_summary(self):
        """Εμφάνιση συνολικής εικόνας"""
        total_income = sum(t["amount"] for t in self.transactions if t["type"] == "Income")
        total_expense = sum(t["amount"] for t in self.transactions if t["type"] == "Expense")
        
        print("\n--- ΟΙΚΟΝΟΜΙΚΟΣ ΑΠΟΛΟΓΙΣΜΟΣ ---")
        print(f"Συνολικά Έσοδα: {total_income}€")
        print(f"Συνολικά Έξοδα: {total_expense}€")
        print(f"Καθαρό Υπόλοιπο: {self.get_balance()}€")

# Παράδειγμα χρήσης:
app = BudgetTracker()

# Προσθήκη εισοδήματος
app.add_transaction("Μισθός", 1500, "Income")

# Προσθήκη εξόδων
app.add_transaction("Ενοίκιο", 500, "Expense")
app.add_transaction("Super Market", 250, "Expense")

# Εμφάνιση αποτελεσμάτων
app.show_summary()
