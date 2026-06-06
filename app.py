import streamlit as st

def check_password():
    # 1. Definimos la contraseña en secrets (igual que hiciste con Supabase)
    def password_entered():
        if st.session_state["password"] == st.secrets["APP_PASSWORD"]:
            st.session_state["password_correct"] = True
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # Pide la contraseña
        st.text_input("Contraseña", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        # Contraseña incorrecta
        st.text_input("Contraseña", type="password", on_change=password_entered, key="password")
        st.error("Contraseña incorrecta")
        return False
    else:
        return True

if check_password():
    st.write("Bienvenido al sistema contable")
    # ... resto de tu app aquí ...

st.set_page_config(page_title="Sistema Contable", layout="wide")

st.sidebar.title("Navegación")
# Al usar la carpeta "pages/", Streamlit crea el menú lateral solo
st.write("Bienvenido al sistema contable centralizado.")
