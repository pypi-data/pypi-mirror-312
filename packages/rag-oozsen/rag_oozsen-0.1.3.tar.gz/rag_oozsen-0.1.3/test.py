#pip install rag-oozsen 
#pip install streamlit 
from rag_oozsen.knowledge_base import build_knowledge_base 
from rag_oozsen.vector_db import summarize_collection 
from rag_oozsen.chat_flow import RAG_LLM, run_rag_pipeline, generateAnswer 
import streamlit as st

def main_basic():
    knowledge_base = build_knowledge_base(r'.\files')
    summarize_collection(knowledge_base)
    run_rag_pipeline(RAG_LLM, knowledge_base)


def main_interface():
    st.title("RAG-OOZSEN Chatbot")
    
    #load knowledge base
    if "knowledge_base" not in st.session_state:
        with st.status("wait: Loading knowledge base...") as status:
            knowledge_base = build_knowledge_base(r'.\files')
            summarize_collection(knowledge_base)
            st.session_state.knowledge_base= knowledge_base
            status.update(label="knowledge base is ready!", state="complete")
    
    #initiate chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    #display chat messages from history on app reload
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    #react to user input
    if prompt := st.chat_input("Write your query here..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        response = generateAnswer(RAG_LLM, st.session_state.knowledge_base, prompt)

        # Display assistant response in chat message container
        with st.chat_message("assistant"):
            st.markdown(response)
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    
if __name__ == "__main__":
    main_basic()
    #main_interface()