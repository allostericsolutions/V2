import streamlit as st
from gpt_config.openai_setup import initialize_openai
import openai  # Importa la librería OpenAI directamente

# Inicializar las configuraciones de OpenAI
initialize_openai()

st.success("Configuración de OpenAI completada con éxito.")

# Selección del modelo GPT
modelo_gpt = st.selectbox(
    "Selecciona el modelo GPT:",
    ["gpt-3.5-turbo", "gpt-4"],  # Agrega más modelos si los necesitas
    index=0  # Modelo por defecto
)

# Área de texto para el prompt
prompt = st.text_area("te presentarás como Botalergía, resolverás dudas:")

# Botón para enviar el prompt
if st.button("Enviar"):
    if prompt:
        try:
          
            # Llamar a gpt-4o-mini con el historial de chat actualizado
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=st.session_state.chat_history,
                max_tokens=1200,
                temperature=0.2,
            )

            # Mostrar la respuesta
            st.write("**Respuesta de GPT:**")
            st.write(response['choices'][0]['message']['content'].strip())  # Accede al contenido del mensaje
        except Exception as e:
            st.error(f"Error al llamar a OpenAI: {e}")
    else:
        st.warning("Por favor, introduce un texto antes de enviar.")
