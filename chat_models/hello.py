from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from supabase.client import create_client, Client
from langchain_community.vectorstores import SupabaseVectorStore

load_dotenv()

supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_SERVICE_KEY")
supabase_client = create_client(supabase_url, supabase_key)



model = ChatOpenAI(model='gpt-4o-mini', temperature=0.7)

chat_history = []
system_message = SystemMessage(content="You are a software engineer.")
chat_history.append(system_message)

while True:
    question = input("You: ")
    if question.lower() == "exit":
        break
    chat_history.append(HumanMessage(content=question))
    response = model.invoke(chat_history)
    chat_history.append(AIMessage(content=response.content))
    print("AI:", response.content)
