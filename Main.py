import streamlit as st
from gpt_config.openai_setup import initialize_openai

def configurar_aplicacion():
  """Inicializa la configuración de OpenAI y devuelve el cliente."""
  try:
    client = initialize_openai()  # Suponiendo que esta función devuelve el cliente OpenAI
    return client
  except Exception as e:
    st.error(f"Error al configurar OpenAI: {e}")
    return None

# Inicializar las configuraciones de OpenAI
client = configurar_aplicacion()

# Verificar si el cliente se inicializó correctamente
if client:
  st.success("Configuración de OpenAI completada con éxito.")
else:
  st.error("Hubo un problema al configurar OpenAI. Revisa la configuración y vuelve a intentarlo.")

# ... Resto de tu código Streamlit ...
