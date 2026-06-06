# ... dentro de tu formulario ...
        btn_guardar = st.form_submit_button("Guardar Cambios")
        
        if btn_guardar:
            datos = {
                "tipo_doi": tipo_doi,
                "doi": doi,
                "nombre1": nombre1,
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
                
                # --- AQUÍ ESTÁ EL TRUCO ---
                st.session_state.persona_a_editar = None # Limpiamos la memoria
                st.rerun() # Recargamos para limpiar el formulario y los estados
                
            except Exception as e:
                st.error(f"Error: {e}")
