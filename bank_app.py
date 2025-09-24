# app.py
import os
from pathlib import Path
import streamlit as st
from sqlalchemy import (
    create_engine, Column, Integer, String, Float, DateTime, ForeignKey, func
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import bcrypt
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import io
from dotenv import load_dotenv

load_dotenv()  # read database URL from .env in production

# ---------- CONFIG ----------
DB_URL = os.getenv("DB_URL", "sqlite:///./bank.db")  # swap to Postgres in prod
Base = declarative_base()
engine = create_engine(DB_URL, connect_args={"check_same_thread": False} if "sqlite" in DB_URL else {})
SessionLocal = sessionmaker(bind=engine)

# ---------- MODELS ----------
class Customer(Base):
    __tablename__ = "customers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    email = Column(String, nullable=False, unique=True)
    mob_no = Column(String, nullable=True)
    account_no = Column(String, nullable=False, unique=True, index=True)
    pin_hash = Column(String, nullable=False)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=func.now())
    transactions = relationship("Transaction", back_populates="customer", cascade="all, delete-orphan")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"))
    amount = Column(Float, nullable=False)
    type = Column(String, nullable=False)  # deposit, withdraw
    timestamp = Column(DateTime, default=func.now())
    note = Column(String, nullable=True)
    customer = relationship("Customer", back_populates="transactions")

Base.metadata.create_all(bind=engine)

# ---------- HELPERS ----------
def hash_pin(pin: str) -> str:
    return bcrypt.hashpw(pin.encode(), bcrypt.gensalt()).decode()

def verify_pin(pin: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(pin.encode(), hashed.encode())
    except Exception:
        return False

def generate_acc_number():
    import random, string
    alpha = random.choices(string.ascii_uppercase, k=4)
    nums = random.choices(string.digits, k=4)
    special = random.choice("!@#$&%^*")
    arr = alpha + nums + [special]
    random.shuffle(arr)
    return "".join(arr)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------- STREAMLIT UI ----------
st.set_page_config(page_title="Secure Bank (Demo)", layout="wide")
st.markdown("<style> .big-font { font-size:22px; } .accent{ color:#0ea5a4; } </style>", unsafe_allow_html=True)
st.title("🏦 Secure Bank — Demo (Streamlit)")

menu = ["Create Account", "Login", "Admin (local)", "About"]
choice = st.sidebar.selectbox("Menu", menu)

# Simple per-session brute-force counter
if "attempts" not in st.session_state:
    st.session_state.attempts = {}

# ---------- CREATE ACCOUNT ----------
if choice == "Create Account":
    st.header("🆕 Create New Account")
    with st.form("create"):
        name = st.text_input("Full Name")
        age = st.number_input("Age", min_value=1, max_value=120, step=1)
        email = st.text_input("Email")
        mob = st.text_input("Mobile Number")
        pin = st.text_input("4-digit PIN", type="password", max_chars=4)
        submitted = st.form_submit_button("Create Account")
        if submitted:
            if not all([name, age, email, pin]) or not (len(pin) == 4 and pin.isdigit()):
                st.error("Please fill all fields and ensure PIN is 4 digits.")
            else:
                db = next(get_db())
                exists = db.query(Customer).filter(Customer.email == email).first()
                if exists:
                    st.error("Account with this email already exists.")
                else:
                    acc_no = generate_acc_number()
                    cust = Customer(
                        name=name, age=int(age), email=email, mob_no=mob,
                        account_no=acc_no, pin_hash=hash_pin(pin), balance=0.0
                    )
                    db.add(cust); db.commit(); db.refresh(cust)
                    st.success(f"Account created! Account Number: {cust.account_no}")
                    st.balloons()

# ---------- LOGIN & DASHBOARD ----------
elif choice == "Login":
    st.header("🔑 Login")
    with st.form("login_form"):
        acc = st.text_input("Account Number")
        pin = st.text_input("PIN", type="password", max_chars=4)
        btn = st.form_submit_button("Login")
        if btn:
            if not (acc and pin and pin.isdigit()):
                st.error("Provide account number and 4-digit PIN.")
            else:
                # rate-limit by session
                attempts = st.session_state.attempts.get(acc, 0)
                if attempts >= 6:
                    st.error("Too many wrong attempts. Contact support.")
                else:
                    db = next(get_db())
                    user = db.query(Customer).filter(Customer.account_no == acc).first()
                    if user and verify_pin(pin, user.pin_hash):
                        st.success("✅ Logged in")
                        st.session_state["user_id"] = user.id
                        st.session_state.attempts[acc] = 0
                    else:
                        st.session_state.attempts[acc] = attempts + 1
                        st.error("Invalid account or PIN.")

    # logged-in area
    if "user_id" in st.session_state:
        db = next(get_db())
        user = db.query(Customer).get(st.session_state.user_id)
        st.subheader(f"Welcome, {user.name} — Balance: ${user.balance:,.2f}")
        col1, col2, col3 = st.columns([2,2,1])
        with col1:
            st.write("### Quick Actions")
            if st.button("Deposit"):
                st.session_state["action"] = "deposit"
            if st.button("Withdraw"):
                st.session_state["action"] = "withdraw"
            if st.button("Logout"):
                st.session_state.pop("user_id", None)
                st.info("Logged out")

        with col2:
            st.write("### Recent Transactions")
            txs = db.query(Transaction).filter(Transaction.customer_id == user.id).order_by(Transaction.timestamp.desc()).limit(10).all()
            if txs:
                df = pd.DataFrame([{"type": t.type, "amt": t.amount, "time": t.timestamp, "note": t.note} for t in txs])
                st.table(df)
            else:
                st.write("No transactions yet.")

        with col3:
            st.write("### Export")
            all_txs = db.query(Transaction).filter(Transaction.customer_id == user.id).order_by(Transaction.timestamp.desc()).all()
            if all_txs:
                df_all = pd.DataFrame([{"type": t.type, "amount": t.amount, "time": t.timestamp, "note": t.note} for t in all_txs])
                csv = df_all.to_csv(index=False).encode()
                st.download_button("Download CSV", data=csv, file_name=f"{user.account_no}_transactions.csv", mime="text/csv")
            else:
                st.write("No data to export.")

        # action forms
        action = st.session_state.get("action")
        if action == "deposit":
            with st.form("deposit_form"):
                amt = st.number_input("Amount to deposit", min_value=1.0, step=0.5)
                note = st.text_input("Note (optional)")
                ok = st.form_submit_button("Confirm Deposit")
                if ok:
                    user.balance += float(amt)
                    tx = Transaction(customer_id=user.id, amount=float(amt), type="deposit", note=note)
                    db.add(tx); db.commit(); db.refresh(user)
                    st.success(f"Deposited ${amt:,.2f}. New balance: ${user.balance:,.2f}")
                    st.session_state.pop("action", None)
        elif action == "withdraw":
            with st.form("withdraw_form"):
                amt = st.number_input("Amount to withdraw", min_value=1.0, step=0.5)
                note = st.text_input("Note (optional)")
                ok = st.form_submit_button("Confirm Withdraw")
                if ok:
                    if amt > user.balance:
                        st.error("Insufficient funds.")
                    else:
                        user.balance -= float(amt)
                        tx = Transaction(customer_id=user.id, amount=float(amt), type="withdraw", note=note)
                        db.add(tx); db.commit(); db.refresh(user)
                        st.success(f"Withdrew ${amt:,.2f}. New balance: ${user.balance:,.2f}")
                        st.session_state.pop("action", None)

        # balance history chart
        st.write("### Balance over time (approx)")
        txs_all = db.query(Transaction).filter(Transaction.customer_id == user.id).order_by(Transaction.timestamp).all()
        if txs_all:
            # build approximate timeseries of balance
            times = []
            balances = []
            bal = 0.0
            for t in txs_all:
                bal = bal + t.amount if t.type == "deposit" else bal - t.amount
                times.append(t.timestamp)
                balances.append(bal)
            fig, ax = plt.subplots(figsize=(8,3))
            ax.plot(times, balances)
            ax.set_ylabel("Balance")
            ax.set_xlabel("Time")
            st.pyplot(fig)
        else:
            st.write("No balance history yet.")

# ---------- ADMIN (local demo only) ----------
elif choice == "Admin (local)":
    st.header("🔧 Admin (Local Demo)")
    pwd = st.text_input("Enter admin code (local)", type="password")
    if pwd == os.getenv("ADMIN_CODE", "admin123"):
        db = next(get_db())
        st.subheader("All users")
        users = db.query(Customer).all()
        df = pd.DataFrame([{"id": u.id, "name": u.name, "email": u.email, "acc": u.account_no, "balance": u.balance} for u in users])
        st.dataframe(df)
        # view transactions
        txs = db.query(Transaction).order_by(Transaction.timestamp.desc()).limit(200).all()
        if txs:
            tdf = pd.DataFrame([{"user_id": t.customer_id, "type": t.type, "amt": t.amount, "time": t.timestamp, "note": t.note} for t in txs])
            st.dataframe(tdf)
        if st.button("Clear demo DB"):
            Base.metadata.drop_all(bind=engine)
            Base.metadata.create_all(bind=engine)
            st.success("Cleared demo DB")
    else:
        st.info("Provide admin code to access demo admin panel.")

# ---------- ABOUT ----------
else:
    st.header("About this demo")
    st.markdown("""
    - Demo purpose only. Not production-grade.
    - PINs are hashed using bcrypt.
    - To make production-ready:
      1. Move DB to Postgres; use migrations (Alembic).
      2. Move business logic to FastAPI; expose secure REST endpoints.
      3. Implement MFA (TOTP), rate-limiting (Redis), defender service for anti-fraud.
      4. Use CI/CD, secrets manager, HTTPS, monitoring and regular security audits.
    """)
