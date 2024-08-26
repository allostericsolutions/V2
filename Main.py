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
      ["gpt-3.5-turbo", "gpt-4"] + ([client.FineTune.list().data[0].fine_tuned_model] if client.FineTune.list().data else []),
      index=0  # Modelo por defecto
  )

  # Ventana de preguntas y respuestas
  st.header("Chat con GPT")
  
  if "mensajes" not in st.session_state:
      st.session_state.mensajes = []

  for mensaje in st.session_state.mensajes:
      st.chat_message(mensaje["rol"]).write(mensaje["contenido"])

  if pregunta := st.chat_input("Escribe tu pregunta aquí..."):
      st.session_state.mensajes.append({"rol": "usuario", "contenido": pregunta})
      st.chat_message("usuario").write(pregunta)  

      try:
          respuesta = client.ChatCompletion.create(
              model=modelo_gpt,
              messages=[
                  {"role": "system", "content": "Eres un útil asistente."},
                  *st.session_state.mensajes  # Incluir historial de mensajes
              ]
          )
          st.session_state.mensajes.append({"rol": "asistente", "contenido": respuesta.choices[0].message.content})
          st.chat_message("asistente").write(respuesta.choices[0].message.content)
      except Exception as e:
          st.error(f"Error al llamar a OpenAI: {e}")

else:
  st.error("Hubo un problema al configurar OpenAI. Revisa la configuración y vuelve a intentarlo.")
