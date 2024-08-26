import openai
import streamlit as st

def initialize_openai():
    """Inicializa OpenAI y configura el cliente para la API V2."""
    OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]
    if not OPENAI_API_KEY:
        st.error("Please add your OpenAI API key to the Streamlit secrets.toml file.")
        st.stop()

    # Configurar el cliente de OpenAI para usar la API V2
    client = openai.OpenAI(api_key=OPENAI_API_KEY, default_headers={"OpenAI-Beta": "assistants=v2"})
    return client
