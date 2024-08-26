import streamlit as st
from gpt_config.openai_setup import initialize_openai

# Inicializar OpenAI usando la función en gpt_config/openai_setup.py
client = initialize_openai()

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

            # Crear un hilo para la conversación usando la API V2
            thread = client.beta.threads.create()
            
            # Agregar el mensaje del usuario al hilo
            client.beta.threads.messages.create(
                thread_id=thread.id,
                role="user",
                content=st.session_state.chat_history
            )

            # Ejecutar el asistente con el modelo seleccionado
            run = client.beta.threads.runs.create(
                thread_id=thread.id,
                assistant_id=modelo_gpt
            )

            # Esperar a que se complete la ejecución
            while run.status != "completed":
                run = client.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
                if run.status in ["failed", "cancelled", "expired", "requires_action"]:
                    st.error(f"Run failed: {run.last_error}")
                    break  # Salir del bucle si hay un error

            # Obtener la respuesta del asistente
            messages = client.beta.threads.messages.list(thread_id=thread.id)
            if not messages.data:
                st.error("No response messages received from the assistant.")
            else:
                # Obtener la respuesta y agregarla al historial
                respuesta_gpt = messages.data[0].content[0].text.value.strip()
                st.session_state.chat_history += f"\nBotalergía: {respuesta_gpt}"

                # Mostrar la respuesta en Streamlit
                st.write("Respuesta de GPT:")
                st.write(respuesta_gpt)

            # Borrar el hilo después de usarlo
            client.beta.threads.delete(thread.id)

        except Exception as e:
            st.error(f"Error al llamar a OpenAI: {e}")
    else:
        st.warning("Por favor, introduce un texto antes de enviar.")
