import streamlit as st
from gpt_config.openai_setup import initialize_openai

def configurar_aplicacion():
    """Inicializa la configuración de OpenAI y devuelve el cliente."""
    try:
        client = initialize_openai()
        return client
    except Exception as e:
        st.error(f"Error al configurar OpenAI: {e}")
        return None

# Inicializar las configuraciones de OpenAI
client = configurar_aplicacion()

if client:
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
                response = client.ChatCompletion.create(
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
else:
    st.error("Hubo un problema al configurar OpenAI. Revisa la configuración y vuelve a intentarlo.")
