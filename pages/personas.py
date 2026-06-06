import streamlit as st
import datetime  # <--- IMPORTANTE: Necesario para manejar fechas
from database import supabase

st.header("👥 Gestión de Personas")

def limpiar(valor):
    return valor if valor is not None else ""

if "persona_a_editar" not in st.session_state:
    st.session_state.persona_a_editar = None

# ... (tab2 se mantiene igual)

with tab1:
    p = st.session_state.persona_a_editar
    
    if p:
        st.info(f"Editando a: {p['nombre_completo']}")
        if st.button("❌ Cancelar edición"):
            st.session_state.persona_a_editar = None
            st.rerun()

    # FORMULARIO
    with st.form("form_persona"):
        col1, col2 = st.columns(2)
        with col1:
            tipo_doi = st.selectbox("Tipo DOI", ["DNI", "RUC", "Pasaporte"], index=0)
            nombre1 = st.text_input("Primer Nombre", value=limpiar(p['nombre1'] if p else ""))
            nombre2 = st.text_input("Segundo Nombre", value=limpiar(p['nombre2'] if p else ""))
            nombre3 = st.text_input("Tercer Nombre", value=limpiar(p['nombre3'] if p else ""))
            apodo = st.text_input("Tercer Nombre", value=limpiar(p['apodo'] if p else ""))
        
        with col2:
            doi = st.text_input("Número DOI", value=limpiar(p['doi'] if p else ""))
            apellido_paterno = st.text_input("Apellido Paterno", value=limpiar(p['apellido_paterno'] if p else ""))
            apellido_materno = st.text_input("Apellido Materno", value=limpiar(p['apellido_materno'] if p else ""))
            
            # Lógica para la fecha
            valor_fecha = None
            if p and p.get('f_nacimiento'):
                # Convertimos string YYYY-MM-DD a objeto fecha
                valor_fecha = datetime.datetime.strptime(p['f_nacimiento'], "%Y-%m-%d").date()
            
            f_nacimiento = st.date_input("Fecha de Nacimiento", value=valor_fecha)
        
        btn_guardar = st.form_submit_button("Guardar Cambios")
        
        if btn_guardar:
            if not nombre1:
                st.error("Primer Nombre es obligatorio.")
            else:
                # Diccionario con la coma corregida
                datos = {
                    "tipo_doi": tipo_doi, "doi": doi, "nombre1": nombre1,
                    "nombre2": nombre2 if nombre2 else None,
                    "nombre3": nombre3 if nombre3 else None,
                    "apellido_paterno": apellido_paterno,
                    "apellido_materno": apellido_materno,
                    "f_nacimiento": str(f_nacimiento) # Convertimos a string para Supabase
                    "apodo": apodo,
                }
                
                try:
                    if p:
                        supabase.table("personas").update(datos).eq("id", p['id']).execute()
                        st.success("¡Registro actualizado!")
                    else:
                        supabase.table("personas").insert(datos).execute()
                        st.success("¡Nueva persona registrada!")
                    
                    st.session_state.persona_a_editar = None
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
