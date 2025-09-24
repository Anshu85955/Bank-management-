import json
import random
import string
from pathlib import Path
import streamlit as st

class Bank:
    dataBase = 'data.json'
    data = []

    # Load data on startup
    try:
        if Path(dataBase).exists():
            with open(dataBase, 'r') as fs:
                data = json.load(fs)
        else:
            data = []
    except Exception as err:
        st.error(f"Error loading database: {err}")
        data = []

    @classmethod
    def __update(cls):
        with open(cls.dataBase, 'w') as fs:
            json.dump(cls.data, fs, indent=4)

    @staticmethod
    def __account_generate():
        alpha = random.choices(string.ascii_uppercase, k=4)
        nums = random.choices(string.digits, k=4)
        spchar = random.choices("!@#$&%^*", k=1)
        acc_id = alpha + nums + spchar
        random.shuffle(acc_id)
        return "".join(acc_id)

    @classmethod
    def create_account(cls, name, age, email, mob, pin):
        if age < 18 or len(str(pin)) != 4:
            return "❌ Sorry, you cannot create an account."

        info = {
            "name": name,
            "age": age,
            "email": email,
            "Mob_no": mob,
            "pin": pin,
            "accountNo": cls.__account_generate(),
            "balance": 0
        }
        cls.data.append(info)
        cls.__update()
        return f"✅ Account created successfully!\nYour Account No: {info['accountNo']}"

    @classmethod
    def deposit(cls, accnumber, pin, amount):
        for user in cls.data:
            if user['accountNo'] == accnumber and user['pin'] == pin:
                if 0 < amount <= 10000:
                    user['balance'] += amount
                    cls.__update()
                    return f"✅ {amount} deposited successfully."
                else:
                    return "❌ Deposit must be between 1 and 10000."
        return "❌ Account not found."

    @classmethod
    def withdraw(cls, accnumber, pin, amount):
        for user in cls.data:
            if user['accountNo'] == accnumber and user['pin'] == pin:
                if 0 < amount <= user['balance']:
                    user['balance'] -= amount
                    cls.__update()
                    return f"✅ {amount} withdrawn successfully."
                else:
                    return "❌ Insufficient balance or invalid amount."
        return "❌ Account not found."

    @classmethod
    def show_details(cls, accnumber, pin):
        for user in cls.data:
            if user['accountNo'] == accnumber and user['pin'] == pin:
                return user
        return None

    @classmethod
    def update_details(cls, accnumber, pin, new_name=None, new_email=None, new_pin=None):
        for user in cls.data:
            if user['accountNo'] == accnumber and user['pin'] == pin:
                if new_name: user['name'] = new_name
                if new_email: user['email'] = new_email
                if new_pin: user['pin'] = int(new_pin)
                cls.__update()
                return "✅ Details updated successfully."
        return "❌ Account not found."

    @classmethod
    def delete(cls, accnumber, pin):
        for user in cls.data:
            if user['accountNo'] == accnumber and user['pin'] == pin:
                cls.data.remove(user)
                cls.__update()
                return "✅ Account deleted successfully."
        return "❌ Account not found."


# ===================== STREAMLIT UI =====================

st.title("🏦 Bank Management System")
menu = ["Create Account", "Deposit Money", "Withdraw Money", "Show Details", "Update Details", "Delete Account"]
choice = st.sidebar.selectbox("Select Operation", menu)

if choice == "Create Account":
    st.header("🆕 Create New Account")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=1)
    email = st.text_input("Email")
    mob = st.text_input("Mobile Number")
    pin = st.text_input("4-Digit PIN", type="password")

    if st.button("Create Account"):
        if name and age and email and mob and pin:
            st.success(Bank.create_account(name, int(age), email, mob, int(pin)))
        else:
            st.error("⚠️ Please fill all fields.")

elif choice == "Deposit Money":
    st.header("💰 Deposit Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)
    if st.button("Deposit"):
        st.success(Bank.deposit(acc, int(pin), int(amount)))

elif choice == "Withdraw Money":
    st.header("💵 Withdraw Money")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    amount = st.number_input("Amount", min_value=1)
    if st.button("Withdraw"):
        st.success(Bank.withdraw(acc, int(pin), int(amount)))

elif choice == "Show Details":
    st.header("📋 Show Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Show"):
        details = Bank.show_details(acc, int(pin))
        if details:
            st.json(details)
        else:
            st.error("❌ Account not found.")

elif choice == "Update Details":
    st.header("✏️ Update Account Details")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    new_name = st.text_input("New Name (optional)")
    new_email = st.text_input("New Email (optional)")
    new_pin = st.text_input("New PIN (optional)")
    if st.button("Update"):
        st.success(Bank.update_details(acc, int(pin), new_name, new_email, new_pin))

elif choice == "Delete Account":
    st.header("🗑️ Delete Account")
    acc = st.text_input("Account Number")
    pin = st.text_input("PIN", type="password")
    if st.button("Delete"):
        st.success(Bank.delete(acc, int(pin)))
