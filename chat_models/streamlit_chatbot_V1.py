from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from supabase import create_client
import uuid
import os
from dotenv import load_dotenv

load_dotenv()


class SUPABASE:
    def __init__(self):
        self.url = os.getenv("SUPABASE_URL")
        self.key = os.getenv("SUPABASE_KEY")
        self.client = create_client(self.url, self.key)

    def insert_message(self, session_id, role, message):
        self.client.table("chat_messages").insert({
            "session_id": session_id,
            "role": role,
            "message": message
        }).execute()


if __name__ == '__main__':
    supabase = SUPABASE()
    # LangChain LLM
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)
    # Start a session
    session_id = str(uuid.uuid4())
    print(f"New session started: {session_id}")

    chat_history = []

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        # Check if the user input is empty
        if not user_input.strip():
            print("Please enter a message.")
            continue

        #insert user message into supabase
        supabase.insert_message(session_id, "user", user_input)

        chat_history.append(HumanMessage(content=user_input))

        # Get bot response
        response = llm(chat_history)
        print("Bot:", response.content)

        # Save bot response
        supabase.insert_message(session_id, "bot", response.content)

        chat_history.append(AIMessage(content=response.content))
