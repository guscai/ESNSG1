import streamlit as st
import datetime
from database import supabase

# Configuración inicial
st.set_page_config(page_title="Gestión de Personas", layout="wide")
st.header("👥 Gestión de Personas")

def limpiar(valor):
    return valor if valor is not None else ""

# Estado de la sesión
if "persona_a_editar" not in st.session_state:
    st.session_state.persona_a_editar = None

tab1, tab2 = st.tabs(["➕ Nuevo / Editar", "🔍 Buscar para Editar"])

# TAB 2: BUSCAR
with tab2:
    query = st.text_input("Buscar por nombre o apellido:")
    if query:
        results = supabase.table("personas").select("*").ilike("nombre_completo", f"%{query}%").execute().data
        for p in results:
            if st.button(f"Editar a {p['nombre_completo']}", key=f"edit_{p['id']}"):
                st.session_state.persona_a_editar = p
                st.rerun()

# TAB 1: EDITAR / CREAR
with tab1:
    p = st.session_state.persona_a_editar
    if p:
        st.info(f"Editando a: {p['nombre_completo']}")
        if st.button("❌ Cancelar edición"):
            st.session_state.persona_a_editar = None
            st.rerun()

    with st.form("form_persona"):
        col1, col2 = st.columns(2)
        with col1:
            tipo_doi = st.selectbox("Tipo DOI", ["DNI", "RUC", "Pasaporte"], index=0)
            nombre1 = st.text_input("Primer Nombre", value=limpiar(p['nombre1'] if p else ""))
            nombre2 = st.text_input("Segundo Nombre", value=limpiar(p['nombre2'] if p else ""))
            nombre3 = st.text_input("Tercer Nombre", value=limpiar(p['nombre3'] if p else ""))
        
        with col2:
            doi = st.text_input("Número DOI", value=limpiar(p['doi'] if p else ""))
            apellido_paterno = st.text_input("Apellido Paterno", value=limpiar(p['apellido_paterno'] if p else ""))
            apellido_materno = st.text_input("Apellido Materno", value=limpiar(p['apellido_materno'] if p else ""))
            
            valor_fecha = None
            if p and p.get('f_nacimiento'):
                try:
                    valor_fecha = datetime.datetime.strptime(p['f_nacimiento'], "%Y-%m-%d").date()
                except:
                    valor_fecha = None
            f_nacimiento = st.date_input("Fecha de Nacimiento", value=valor_fecha)
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            btn_guardar = st.form_submit_button("Guardar Cambios")
        with col_btn2:
            btn_eliminar_form = st.form_submit_button("🗑️ Eliminar Registro", type="primary") if p else None
        
        # Guardar
        if btn_guardar:
            if not nombre1 or not apellido_paterno:
                st.error("Primer Nombre y Apellido Paterno son obligatorios.")
            else:
                datos = {
                    "tipo_doi": tipo_doi, "doi": doi, "nombre1": nombre1,
                    "nombre2": nombre2 if nombre2 else None,
                    "nombre3": nombre3 if nombre3 else None,
                    "apellido_paterno": apellido_paterno,
                    "apellido_materno": apellido_materno,
                    "f_nacimiento": str(f_nacimiento)
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

        # Eliminar desde el formulario
        if btn_eliminar_form and p:
            supabase.table("personas").delete().eq("id", p['id']).execute()
            st.session_state.persona_a_editar = None
            st.rerun()

# TABLA DE ELIMINACIÓN DIRECTA
st.divider()
st.subheader("📋 Registros Guardados")

registros = supabase.table("personas").select("*").execute().data

for registro in registros:
    c1, c2 = st.columns([4, 1])
    with c1:
        st.write(f"ID {registro['id']} | **{registro.get('nombre_completo', 'Sin nombre')}**")
    with c2:
        if st.button("🗑️ Borrar", key=f"del_{registro['id']}"):
            st.session_state.confirmar_id = registro['id']
            st.rerun()

# Lógica de confirmación
if "confirmar_id" in st.session_state:
    id_conf = st.session_state.confirmar_id
    st.warning(f"¿Confirmas borrar el registro ID {id_conf}?")
    if st.button("✅ Confirmar Borrado"):
        supabase.table("personas").delete().eq("id", id_conf).execute()
        del st.session_state.confirmar_id
        st.rerun()
    if st.button("❌ Cancelar"):
        del st.session_state.confirmar_id
        st.rerun()
