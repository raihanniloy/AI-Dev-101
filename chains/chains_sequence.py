from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableSequence
load_dotenv()

if __name__ == '__main__':
    model = ChatOpenAI(model='gpt-4o-mini', temperature=.7)

    system_message = "you are a private investigator. You are very smart and you solve every case"
    template = "Answer the question as if you are a detective. You are very smart and you solve every case. {input}"
    prompt = ChatPromptTemplate([
        ("system", "you are a private investigator. You are very smart and you solve every case"),
        ("human", "Answer the question as if you are a detective. You are very smart and you solve every case. {input}"),
    ])


    # chain = prompt | model | StrOutputParser()

    format_prompt = RunnableLambda(lambda x: prompt.format_prompt(**x))
    invoke_model = RunnableLambda(lambda x: model.invoke(x.to_messages()))
    parse_output = RunnableLambda(lambda x: x.content)

    chain = RunnableSequence(first=format_prompt, middle=[invoke_model], last=parse_output)

    result = chain.invoke({"input": "What is the capital of France?"})
    print(result)
