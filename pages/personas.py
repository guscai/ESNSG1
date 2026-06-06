import streamlit as st
import datetime
from database import supabase

# 1. Configuración de página
st.set_page_config(page_title="Gestión de Personas", layout="wide")
st.header("👥 Gestión de Personas")

def limpiar(valor):
    return valor if valor is not None else ""

# 2. Estado de la sesión
if "persona_a_editar" not in st.session_state:
    st.session_state.persona_a_editar = None

# 3. Navegación
tab1, tab2 = st.tabs(["➕ Nuevo / Editar", "🔍 Buscar para Editar"])

with tab2:
    query = st.text_input("Buscar por nombre o apellido:")
    if query:
        results = supabase.table("personas").select("*").ilike("nombre_completo", f"%{query}%").execute().data
        for p in results:
            if st.button(f"Editar a {p['nombre_completo']}", key=f"edit_{p['id']}"):
                st.session_state.persona_a_editar = p
                st.rerun()

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
        
        col_b1, col_b2 = st.columns(2)
        with col_b1:
            btn_guardar = st.form_submit_button("Guardar Cambios")
        with col_b2:
            btn_eliminar = st.form_submit_button("🗑️ Eliminar Registro", type="primary") if p else None
        
        if btn_guardar:
            if not nombre1 or not apellido_paterno:
                st.error("El Primer Nombre y Apellido Paterno son obligatorios.")
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

        if btn_eliminar and p:
            supabase.table("personas").delete().eq("id", p['id']).execute()
            st.session_state.persona_a_editar = None
            st.rerun()

# 4. Tabla Profesional
st.divider()
st.subheader("📋 Registros Guardados")
registros = supabase.table("personas").select("*").execute().data

# Añadimos una columna 'borrar' temporal para la tabla
for r in registros:
    r['borrar'] = False

edited_df = st.data_editor(
    registros,
    column_config={
        "id": st.column_config.NumberColumn("ID", disabled=True),
        "borrar": st.column_config.CheckboxColumn("¿Borrar?", default=False)
    },
    hide_index=True,
    use_container_width=True
)

if st.button("🗑️ Eliminar seleccionados"):
    ids_a_borrar = [r['id'] for r in edited_df if r.get('borrar') == True]
    if ids_a_borrar:
        for id_b in ids_a_borrar:
            supabase.table("personas").delete().eq("id", id_b).execute()
        st.rerun()
    else:
        st.warning("Selecciona al menos una fila marcando el checkbox '¿Borrar?'.")
