# database.py
from supabase import create_client
import streamlit as st

url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

def insertar_persona(data):
    return supabase.table("personas").insert(data).execute()

def obtener_personas():
    return supabase.table("personas").select("*").execute().data
