import streamlit as st
import pandas as pd

st.set_page_config(page_title="Chassis Budget App", layout="wide")

st.title("🏎️ Chassis ECU Budget Commander")

# --- MASTER DATA ---
if 'ecus' not in st.session_state:
    st.session_state.ecus = ["EDC", "EPAS", "ABS", "Torque Vectoring"]

with st.sidebar:
    st.header("⚙️ Admin")
    new_ecu = st.text_input("Aggiungi nuova ECU")
    if st.button("Aggiungi"):
        st.session_state.ecus.append(new_ecu)
        st.rerun()

# --- PREMESSE ---
st.header("1. Premesse Tecniche")
c1, c2, c3 = st.columns(3)
arch = c1.selectbox("Architettura EE", ["Zonale", "Centralizzata"])
pwr = c2.selectbox("Layout Powertrain", ["BEV", "PHEV", "ICE"])
susp = c3.selectbox("Sospensioni", ["Attive", "Semi-attive", "Passive"])

# --- COSTI ---
st.header("2. Costificazione ECU")
sel_ecu = st.selectbox("Seleziona ECU dal Menù", st.session_state.ecus)

fasi = ["SW Release", "Project Mgmt", "Requirement", "SW Dev", "SW Testing", "Vehicle Test"]
cat_list = ["HC", "ZBB", "KUE", "Esterno"]

costi = {}
for fase in fasi:
    col_f, col_c, col_v = st.columns([2, 1, 1])
    col_f.write(f"**{fase}**")
    t = col_c.selectbox(f"Tipo", cat_list, key=f"t_{fase}")
    v = col_v.number_input(f"Valore (€)", min_value=0, key=f"v_{fase}")
    costi[fase] = {"Categoria": t, "Valore": v}

if st.button("Calcola Totale"):
    tot = sum(item["Valore"] for item in costi.values())
    st.metric(f"Totale per {sel_ecu}", f"€ {tot:,.2f}")
