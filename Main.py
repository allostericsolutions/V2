import streamlit as st
from gpt_config.openai_setup import initialize_openai
import openai

# Inicializar las configuraciones de OpenAI
openai.api_key = initialize_openai() 

st.success("Configuración de OpenAI completada con éxito.")

# Selección del modelo GPT
modelo_gpt = st.selectbox(
    "Selecciona el modelo GPT:",
    ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"],  
    index=0
)

# Área de texto para el prompt
prompt = st.text_area("Te presentarás como Botalergía, resolverás dudas:")

# Historial de la conversación
if "chat_history" not in st.session_state:
    st.session_state.chat_history = "Eres Botalergía, un experto en alergias."

# Botón para enviar el prompt
if st.button("Enviar"):
    if prompt:
        try:
            # Agregar la pregunta del usuario al historial
            st.session_state.chat_history += f"\nUsuario: {prompt}"

            # Llamar a la API de OpenAI (usando el endpoint 'completions')
            response = openai.Completion.create(
                model=modelo_gpt,
                prompt=st.session_state.chat_history,
                max_tokens=1200,
                temperature=0.2,
            )

            # Obtener la respuesta del modelo
            respuesta_gpt = response.choices[0].text.strip()

            # Agregar la respuesta de GPT al historial
            st.session_state.chat_history += f"\nBotalergía: {respuesta_gpt}"

            # Mostrar la respuesta en Streamlit
            st.write("**Respuesta de GPT:**")
            st.write(respuesta_gpt)

        except Exception as e:
            st.error(f"Error al llamar a OpenAI: {e}")
    else:
        st.warning("Por favor, introduce un texto antes de enviar.")
