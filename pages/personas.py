import streamlit as st
from database import supabase

st.header("👥 Gestión de Personas")

def limpiar(valor):
    return valor if valor is not None else ""

if "persona_a_editar" not in st.session_state:
    st.session_state.persona_a_editar = None

tab1, tab2 = st.tabs(["➕ Nuevo / Editar", "🔍 Buscar para Editar"])

with tab2:
    query = st.text_input("Buscar por nombre o apellido:")
    if query:
        results = supabase.table("personas").select("*").ilike("nombre_completo", f"%{query}%").execute().data
        for p in results:
            if st.button(f"Editar a {p['nombre_completo']}", key=str(p['id'])):
                st.session_state.persona_a_editar = p
                st.rerun()

with tab1:
    p = st.session_state.persona_a_editar
    
    if p:
        st.info(f"Editando a: {p['nombre_completo']}")
        if st.button("❌ Cancelar edición"):
            st.session_state.persona_a_editar = None
            st.rerun()

    # Añadimos clear_on_submit=True para limpiar los campos automáticamente
    with st.form("form_persona", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            tipo_doi = st.selectbox("Tipo DOI", ["DNI", "RUC", "Pasaporte"], 
                                    index=["DNI", "RUC", "Pasaporte"].index(p['tipo_doi']) if p else 0)
            nombre1 = st.text_input("Primer Nombre", value=limpiar(p['nombre1'] if p else ""))
            nombre2 = st.text_input("Segundo Nombre", value=limpiar(p['nombre2'] if p else ""))
            nombre3 = st.text_input("Tercer Nombre", value=limpiar(p['nombre3'] if p else ""))
        
        with col2:
            doi = st.text_input("Número DOI", value=limpiar(p['doi'] if p else ""))
            apellido_paterno = st.text_input("Apellido Paterno", value=limpiar(p['apellido_paterno'] if p else ""))
            apellido_materno = st.text_input("Apellido Materno", value=limpiar(p['apellido_materno'] if p else ""))
        
        # El botón DEBE estar dentro del 'with st.form'
        btn_guardar = st.form_submit_button("Guardar Cambios")
        
        # La lógica de guardado debe estar dentro del 'with st.form'
        if btn_guardar:
            if not nombre1 or not apellido_paterno:
                st.error("Por favor, completa al menos el Primer Nombre y Apellido Paterno.")
            else:
                datos = {
                    "tipo_doi": tipo_doi, "doi": doi, "nombre1": nombre1,
                    "nombre2": nombre2 if nombre2 else None,
                    "nombre3": nombre3 if nombre3 else None,
                    "apellido_paterno": apellido_paterno,
                    "apellido_materno": apellido_materno
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
                    st.error(f"Error de base de datos: {e}")

st.divider()
st.subheader("📋 Registros Guardados")
st.dataframe(supabase.table("personas").select("*").execute().data)
