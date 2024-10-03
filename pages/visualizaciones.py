import streamlit as st
import json
import pandas as pd
import os

# Nombre del archivo JSON
JSON_FILE = 'data.json'

# Función para cargar el JSON
def load_data():
    if os.path.exists(JSON_FILE):
        with open(JSON_FILE, 'r') as f:
            data = json.load(f)
    else:
        data = {"cuentas": []}
    return data

st.title("Visualizaciones de Cuentas")

data = load_data()

# Total general
total_general = sum([cuenta["saldo_total"] for cuenta in data["cuentas"]])
st.metric(label="Total General", value=f"${total_general:,.2f}")

# Aperturado de totales por cuenta
st.subheader("Totales por cuenta")
df_cuentas = pd.DataFrame(data["cuentas"])
st.dataframe(df_cuentas[["cuenta", "saldo_total"]], hide_index=True)

# Movimientos por cuenta
st.subheader("Movimientos por cuenta")
for cuenta in data["cuentas"]:
    st.write(f"Cuenta: {cuenta['cuenta']}")
    df_movimientos = pd.DataFrame(cuenta["movimientos"])
    if not df_movimientos.empty:
        st.dataframe(df_movimientos, hide_index=True)
    else:
        st.write("No hay movimientos.")

# Gastos por categoría
st.subheader("Gastos por categoría")
categorias = {}
for cuenta in data["cuentas"]:
    for movimiento in cuenta["movimientos"]:
        if movimiento["categoria"] in categorias:
            categorias[movimiento["categoria"]] += movimiento["monto"]
        else:
            categorias[movimiento["categoria"]] = movimiento["monto"]

df_categorias = pd.DataFrame(list(categorias.items()), columns=["Categoría", "Monto"])
st.bar_chart(df_categorias.set_index("Categoría"))