import streamlit as st
from database import insertar_persona  # Importa la función de tu archivo modular

st.header("👥 Registrar Nueva Persona")

with st.form("registro_persona"):
    col1, col2 = st.columns(2)
    with col1:
        tipo_doi = st.selectbox("Tipo de documento", ["DNI", "RUC", "Pasaporte"])
        nombre1 = st.text_input("Primer Nombre")
        nombre2 = st.text_input("Segundo Nombre")
    with col2:
        doi = st.text_input("Número de documento")
        apellido_paterno = st.text_input("Apellido Paterno")
        apellido_materno = st.text_input("Apellido Materno")

    submitted = st.form_submit_button("Guardar en Supabase")

    if submitted:
        if nombre1 and apellido_paterno and doi:
            data = {
                "tipo_doi": tipo_doi,
                "doi": doi,
                "nombre1": nombre1,
                "nombre2": nombre2,
                "apellido_paterno": apellido_paterno,
                "apellido_materno": apellido_materno
            }
            try:
                insertar_persona(data)
                st.success("¡Datos guardados correctamente!")
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Completa los campos obligatorios.")
