import streamlit as st

# Configuración del título de la página
st.set_page_config(page_title="Control Contable", page_icon="📊")
st.title("🧮 Lógica Contable Automatizada")

st.markdown("### Ingrese los datos de la transferencia:")

# Campos de entrada de texto y números
origen = st.text_input("Cuenta Origen (Desde):", placeholder="Ej. Caja Chica, Banco X")
destino = st.text_input("Cuenta Destino (Hacia):", placeholder="Ej. Proveedores, Gastos de Envío")
monto = st.number_input("Monto ($):", min_value=0.0, format="%.2f", step=10.0)
repeticiones = st.number_input("Veces de repetición (Frecuencia):", min_value=1, step=1, value=1)

# Espacio visual
st.write("---")

# Botón para ejecutar la acción
if st.button("Procesar Transacciones", type="primary"):
    if origen and destino and monto > 0:
        st.success(f"✅ Generando {repeticiones} asiento(s) contable(s) con éxito:")
        
        # Lógica de repetición contable (Simulación de Libro Diario)
        for i in range(1, int(repeticiones) + 1):
            st.info(f"🔄 **Asiento #{i}:** Se debitaron **${monto:.2f}** de *{origen}* y se acreditaron en *{destino}*.")
    else:
        st.error("⚠️ Por favor, asegúrate de llenar las cuentas y que el monto sea mayor a 0.")

