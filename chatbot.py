from openai import OpenAI
import streamlit as st

# access the environment variables
ai_endpoint_model = "Mixtral-8x7B-Instruct-v0.1"
ai_endpoint_url = "https://mixtral-8x7b-instruct-v01.endpoints.kepler.ai.cloud.ovh.net/api/openai_compat/v1"
ai_endpoint_token = "ADD YOUR TOKEN"

# Streamlit interface
with st.container():
    st.title("💬 Assistant Chatbot")

messages_container = st.container()

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "system", 
                                     "content": "Je suis AVA, un assistant intelligent et bienveillant!", 
                                     "avatar": "🤖"}]

# Affichage des messages précédents
with messages_container:
    for msg in st.session_state.messages:
        st.chat_message(msg["role"], avatar=msg["avatar"]).write(msg["content"])

# Saisie utilisateur
user_input = st.chat_input("Inter your message...")
if user_input:
    client = OpenAI(
                    base_url=ai_endpoint_url, 
                    api_key=ai_endpoint_token
                   )
    st.session_state.messages.append({"role": "user", "content": user_input, "avatar": "👤"})
    
    with messages_container:
        st.chat_message("user", avatar="👤").write(user_input)
    
    response = client.chat.completions.create(
        model=ai_endpoint_model, 
        messages=st.session_state.messages,
        temperature=0,
        max_tokens=1024,
    )
    
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "system", "content": msg, "avatar": "🤖"})
    
    with messages_container:
        st.chat_message("system", avatar="🤖").write(msg)
