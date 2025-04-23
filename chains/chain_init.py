from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
load_dotenv()

if __name__ == '__main__':
    model = ChatOpenAI(model='gpt-4o-mini', temperature=.7)

    system_message = "you are a private investigator. You are very smart and you solve every case"
    template = "Answer the question as if you are a detective. You are very smart and you solve every case. {input}"
    prompt = ChatPromptTemplate([
        ("system", "you are a private investigator. You are very smart and you solve every case"),
        ("human", "Answer the question as if you are a detective. You are very smart and you solve every case. {input}"),
    ])

    chain = prompt | model | StrOutputParser()
    result = chain.invoke({"input": "What is the capital of France?"})
    print(result)
