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
        
        # --- AQUÍ LA MODIFICACIÓN: Columnas para los botones ---
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            btn_guardar = st.form_submit_button("Guardar Cambios")
        with col_btn2:
            # Solo mostramos el botón si estamos editando un registro (p es True)
            btn_eliminar = st.form_submit_button("🗑️ Eliminar Registro", type="primary") if p else None
        
        # Lógica de guardado
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

        # --- Lógica de eliminación ---
        if btn_eliminar:
            try:
                supabase.table("personas").delete().eq("id", p['id']).execute()
                st.warning("Registro eliminado correctamente.")
                st.session_state.persona_a_editar = None
                st.rerun()
            except Exception as e:
                st.error(f"Error al eliminar: {e}")
