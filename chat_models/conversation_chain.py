import os
import uuid
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from supabase import create_client, Client

# Load environment variables
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

    # Init Supabase
    supabase = SUPABASE()
    # Generate a unique session_id per user/session
    session_id = str(uuid.uuid4())

    # LangChain setup
    llm = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)
    memory = ConversationBufferMemory(return_messages=True)
    conversation = ConversationChain(llm=llm, memory=memory, verbose=True)

    # Chat loop
    print("Chat with the bot! Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break

        # Save user message
        #supabase.insert_message(session_id, "user", user_input)

        # Get bot reply
        response = conversation.predict(input=user_input)

        print("Bot:", response)

        # Save bot message
        #supabase.insert_message(session_id, "bot", response)
