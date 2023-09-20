from dotenv import load_dotenv
import streamlit as st
from FileParser import get_texts_from_files
from StyleTemplate import css, bot_template, user_template
from activity_agent import SharedActivityAgent
    
def add_log(log: str):
    print(log)
    if st.session_state.logs is None:
        logs = [log]
        st.session_state.logs = logs
    else:
        st.session_state.logs.append(log)
        
def main():
    load_dotenv()
    st.set_page_config("Ask me any thing")
    st.write(css, unsafe_allow_html=True)
    st.header("Ask your questions :)")
    if "role" not in st.session_state:
        st.session_state.role = None
        
    if "agent" not in st.session_state:
        activityAgent = SharedActivityAgent
        st.session_state.agent = activityAgent
        
    # Implementing the side bar
    with st.sidebar:
        st.subheader("Upload your documents")
        files = st.file_uploader("Upload your PDFs or Docx files", type=["pdf","docx"], accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Loading files"):
                add_log("> Files Loaded")
                text = get_texts_from_files(files)
                st.session_state.text = text
                st.session_state.agent.initialize_vector_store(text)
            
    if "conversation" in st.session_state:
        if st.session_state.role is None:
            role = st.text_input("Enter your role")
            if st.button("Save Role"):
                add_log(f'> Role saved is {role}!')
                st.session_state.agent.save_role(role)
                st.session_state.role = role
        else:
            input = st.text_input("As me anything")
            if st.button("Send"):
                st.subheader("Logs:")
                
                response = st.session_state.agent.ask_question(input)
                st.subheader("Chat")
                for item in response["conversation"]:
                    st.write(user_template.replace("{{MSG}}", item["question"]), unsafe_allow_html=True)
                    st.write(bot_template.replace("{{MSG}}", item["answer"]), unsafe_allow_html=True)
                
if __name__ == '__main__':
    main()