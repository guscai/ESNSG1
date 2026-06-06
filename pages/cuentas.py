
import streamlit as st
from utils_forms import render_form_y_tabla

nombre_de_la_pagina = "👥 Cuentas"


# Define los campos de esta tabla específica
configuracion = {
    "nom_cta": "text",
}

# Llama a la función genérica
render_form_y_tabla("cuentas", configuracion)
