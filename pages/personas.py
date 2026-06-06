import streamlit as st
from database import supabase # Asegúrate de importar tu cliente configurado

st.header("👥 Gestión de Personas")

# 1. Estado inicial para manejar la edición
if "persona_a_editar" not in st.session_state:
    st.session_state.persona_a_editar = None

# 2. Rectángulo Superior (Búsqueda y Formulario)
tab1, tab2 = st.tabs(["➕ Nuevo / Editar", "🔍 Buscar para Editar"])

with tab2:
    query = st.text_input("Buscar por nombre o apellido:")
    if query:
        # Buscamos en la base de datos
        results = supabase.table("personas").select("*").ilike("nombre_completo", f"%{query}%").execute().data
        for p in results:
            if st.button(f"Editar a {p['nombre_completo']}", key=p['id']):
                st.session_state.persona_a_editar = p
                st.rerun()

with tab1:
    # Si hay alguien en session_state, cargamos sus datos, si no, campos vacíos
    p = st.session_state.persona_a_editar
    
    with st.form("form_persona", clear_on_submit=True):
        col1, col2 = st.columns(2)
        nombre1 = col1.text_input("Nombre", value=p['nombre1'] if p else "")
        apellido = col2.text_input("Apellido", value=p['apellido_paterno'] if p else "")
        
        btn_guardar = st.form_submit_button("Guardar Cambios")
        
        if btn_guardar:
            # Lógica: Si p existe, hacemos UPDATE, si no, INSERT
            if p:
                supabase.table("personas").update({"nombre1": nombre1}).eq("id", p['id']).execute()
            else:
                supabase.table("personas").insert({"nombre1": nombre1, ...}).execute()
            st.session_state.persona_a_editar = None
            st.rerun()

# 3. Rectángulo Inferior (Tabla de registros)
st.divider()
st.subheader("📋 Registros Guardados")
data = supabase.table("personas").select("*").execute().data
st.table(data)
