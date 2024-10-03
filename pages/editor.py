import streamlit as st
import json
import os
from datetime import datetime

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

# Función para guardar el JSON
def save_data(data):
    with open(JSON_FILE, 'w') as f:
        json.dump(data, f, indent=4)

st.title("Editor de Cuentas y Movimientos")

data = load_data()

# Mostrar cuentas existentes
st.subheader("Cuentas Existentes")
if data["cuentas"]:
    selected_account = st.selectbox("Selecciona una cuenta para editar o eliminar", [cuenta['cuenta'] for cuenta in data['cuentas']])
    
    cuenta_data = next(cuenta for cuenta in data["cuentas"] if cuenta["cuenta"] == selected_account)
    
    # Mostrar información de la cuenta seleccionada
    st.write(f"Saldo: {cuenta_data['saldo_total']}")

    # Botón para eliminar la cuenta
    if st.button(f"Eliminar cuenta {selected_account}"):
        data["cuentas"] = [cuenta for cuenta in data["cuentas"] if cuenta["cuenta"] != selected_account]
        save_data(data)
        st.success(f"Cuenta {selected_account} eliminada.")
    
    # Modificar saldo de la cuenta seleccionada
    nuevo_saldo = st.number_input("Nuevo saldo", value=cuenta_data["saldo_total"], step=0.01)
    if st.button("Modificar saldo"):
        cuenta_data["saldo_total"] = nuevo_saldo
        save_data(data)
        st.success("Saldo actualizado.")
    
    # Agregar movimiento
    st.subheader("Agregar Movimiento")
    fecha = st.date_input("Fecha", value=datetime.now())
    categoria = st.text_input("Categoría")
    descripcion = st.text_input("Descripción")
    monto = st.number_input("Monto", step=0.01)
    
    if st.button("Agregar movimiento"):
        nuevo_movimiento = {
            "fecha": fecha.strftime("%Y-%m-%d"),
            "categoria": categoria,
            "descripcion": descripcion,
            "monto": monto
        }
        cuenta_data["movimientos"].append(nuevo_movimiento)
        save_data(data)
        st.success("Movimiento agregado.")
else:
    st.write("No hay cuentas registradas.")

# Agregar una nueva cuenta
st.subheader("Agregar una Nueva Cuenta")
cuenta_name = st.text_input("Nombre de la cuenta")
saldo_inicial = st.number_input("Saldo inicial", min_value=0.0, step=0.01)

if st.button("Agregar cuenta"):
    nueva_cuenta = {
        "cuenta": cuenta_name,
        "saldo_total": saldo_inicial,
        "movimientos": []
    }
    data["cuentas"].append(nueva_cuenta)
    save_data(data)
    st.success(f"Cuenta {cuenta_name} agregada con éxito.")

# Visualizador del JSON
st.subheader("Visualizador del JSON")

json_str = json.dumps(data, indent=2, ensure_ascii=False)
st.code(json_str, language="json")
