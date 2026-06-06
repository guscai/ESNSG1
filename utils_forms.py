import streamlit as st
import datetime
from database import supabase

def render_form_y_tabla(nombre_tabla, campos_config, primary_key="id"):
    """
    nombre_tabla: string, nombre en Supabase
    campos_config: dict {campo: tipo}, ej: {"nombre1": "text", "f_nacimiento": "date"}
    """
    
    # --- FORMULARIO ---
    with st.form(f"form_{nombre_tabla}"):
        cols = st.columns(2)
        datos = {}
        
        # Generar inputs dinámicos
        for i, (campo, tipo) in enumerate(campos_config.items()):
            col = cols[i % 2]
            label = campo.replace("_", " ").capitalize()
            if tipo == "text":
                datos[campo] = col.text_input(label)
            elif tipo == "date":
                datos[campo] = str(col.date_input(label))
            elif tipo == "select":
                datos[campo] = col.selectbox(label, ["DNI", "RUC", "Pasaporte"])
        
        if st.form_submit_button("Guardar"):
            try:
                supabase.table(nombre_tabla).insert(datos).execute()
                st.success("Guardado correctamente")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")

    # --- TABLA Y BORRADO ---
    st.subheader(f"Registros en {nombre_tabla.capitalize()}")
    registros = supabase.table(nombre_tabla).select("*").execute().data
    
    if registros:
        for r in registros:
            r['borrar'] = False
            
        edited_df = st.data_editor(
            registros,
            column_config={"borrar": st.column_config.CheckboxColumn("¿Borrar?")},
            hide_index=True
        )
        
        if st.button("🗑️ Eliminar seleccionados", key=f"del_{nombre_tabla}"):
            ids = [r[primary_key] for r in edited_df if r.get('borrar') == True]
            for id_b in ids:
                supabase.table(nombre_tabla).delete().eq(primary_key, id_b).execute()
            st.rerun()
