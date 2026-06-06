import streamlit as st
from supabase import create_client

# Configuración usando Streamlit Secrets (lo que configuraste en la nube)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

def insertar_persona(data):
    return supabase.table("personas").insert(data).execute()
