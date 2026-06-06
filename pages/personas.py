import streamlit as st
from database import supabase

st.header("👥 Gestión de Personas")

# Estado inicial para edición
if "persona_a_editar" not in st.session_state:
    st.session_state.persona_a_editar = None

# Tabs para el layout
tab1, tab2 = st.tabs(["➕ Nuevo / Editar", "🔍 Buscar para Editar"])

with tab2:
    query = st.text_input("Buscar por nombre:")
    if query:
        # Buscamos en la base de datos
        results = supabase.table("personas").select("*").ilike("nombre_completo", f"%{query}%").execute().data
        for p in results:
            if st.button(f"Editar a {p['nombre_completo']}", key=str(p['id'])):
                st.session_state.persona_a_editar = p
                st.rerun()

with tab1:
    p = st.session_state.persona_a_editar
    with st.form("form_persona", clear_on_submit=True):
        nombre1 = st.text_input("Nombre", value=p['nombre1'] if p else "")
        apellido = st.text_input("Apellido", value=p['apellido_paterno'] if p else "")
        btn_guardar = st.form_submit_button("Guardar")
        
        if btn_guardar:
            if p:
                supabase.table("personas").update({"nombre1": nombre1, "apellido_paterno": apellido}).eq("id", p['id']).execute()
            else:
                supabase.table("personas").insert({"nombre1": nombre1, "apellido_paterno": apellido, "tipo_doi": "DNI", "doi": "0000"}).execute()
            st.session_state.persona_a_editar = None
            st.rerun()

st.divider()
st.subheader("📋 Registros")
data = supabase.table("personas").select("*").execute().data
st.dataframe(data)
