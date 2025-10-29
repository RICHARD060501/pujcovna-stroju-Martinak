
import streamlit as st
import sqlite3
import pandas as pd

# Připojení k databázi
def get_connection():
    return sqlite3.connect("rental.db")

def get_clients():
    conn = get_connection()
    df = pd.read_sql_query("SELECT name, discount FROM clients", conn)
    conn.close()
    return df

def get_machines():
    conn = get_connection()
    df = pd.read_sql_query("SELECT name, price_per_day, available FROM machines", conn)
    conn.close()
    return df

st.set_page_config(page_title="Půjčovna stavebních strojů", page_icon="🏗️", layout="centered")

st.title("🏗️ Půjčovna stavebních strojů")
st.markdown("---")

# Načtení dat
clients = get_clients()
machines = get_machines()

# Formulář
st.header("🧾 Výpočet půjčovného")
client_name = st.selectbox("Vyberte klienta:", clients["name"])
machine_name = st.selectbox("Vyberte stroj:", machines["name"])
days = st.number_input("Počet dní:", min_value=1, step=1)

# Získání slevy a ceny
discount = clients.loc[clients["name"] == client_name, "discount"].values[0]
price_per_day = machines.loc[machines["name"] == machine_name, "price_per_day"].values[0]
available = machines.loc[machines["name"] == machine_name, "available"].values[0]

if available == 0:
    st.error("❌ Tento stroj je momentálně nedostupný.")
else:
    total_price = days * price_per_day * (1 - discount / 100)
    st.success(f"💰 Celková cena půjčovného: **{total_price:.2f} Kč** (sleva {discount} %)")

st.markdown("---")
st.caption("Vytvořil ChatGPT – verze pro Streamlit Cloud")
