
import streamlit as st
from utils_forms import render_form_y_tabla

st.header("👥 Gestión de Personas")

# Define los campos de esta tabla específica
configuracion = {
    "nom_cta": "text",
}

# Llama a la función genérica
render_form_y_tabla("cuentas", configuracion)
