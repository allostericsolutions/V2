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
prompt = st.text_area("Introduce tu texto aquí:")

# Botón para enviar el prompt
if st.button("Enviar"):
    if prompt:
        try:
            # Llamada a la API de OpenAI (formato de mensajes)
            response = openai.ChatCompletion.create(
                model=modelo_gpt,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,  # Ajusta según la longitud de respuesta deseada
                temperature=0.7,  # Ajusta la temperatura según tus preferencias
            )

            # Mostrar la respuesta
            st.write("**Respuesta de GPT:**")
            st.write(response['choices'][0]['message']['content'].strip())  # Accede al contenido del mensaje
        except Exception as e:
            st.error(f"Error al llamar a OpenAI: {e}")
    else:
        st.warning("Por favor, introduce un texto antes de enviar.")
