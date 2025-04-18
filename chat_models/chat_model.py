from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from supabase.client import create_client
from langchain_community.vectorstores import SupabaseVectorStore
import streamlit as st
import os

load_dotenv()
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase_client = create_client(supabase_url, supabase_key)


class ChatModel:
    def __init__(self):
        self.chat_history = []
        self.system_message = SystemMessage(content="Your name is Bongo Boltu. You are a corrupt leader who screams at his minions like they are his slaves. Also you speak in bengali. Also you use bangla slang in every reply. You have a daughter named Hasina. You always praise her in your every reply for being a good dictator and good slave master")
        self.chat_history.append(self.system_message)
        self.model = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)

    def ask_question(self, question):
        self.chat_history.append(HumanMessage(content=question))
        response = self.model.invoke(self.chat_history)
        self.chat_history.append(AIMessage(content=response.content))
        return response.content

    def clear_chat(self):
        self.chat_history = []
        self.chat_history.append(self.system_message)


if __name__ == '__main__':
    chat_model = ChatModel()
    while True:
        question = input("You: ")
        if question.lower() == "exit":
            break
        response = chat_model.ask_question(question)
        print("Bongo Boltu:", response)