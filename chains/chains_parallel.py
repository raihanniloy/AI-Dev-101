from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnableLambda, RunnableSequence, RunnableParallel
from langchain.schema.output_parser import StrOutputParser
load_dotenv()

if __name__ == '__main__':
    model = ChatOpenAI(model='gpt-4o-mini', temperature=.7, streaming=True)

    system_message = "You are a product Manager. You will find the pros and cons of a product."
    template = "Please find review the following product: {input}"
    prompt = ChatPromptTemplate([
        ("system", system_message),
        ("human", template),
    ])

    pros_prompt = ChatPromptTemplate([
        ("system", system_message),
        ("human", "find the pros features from this features: {features}"),
    ])

    cons_prompt = ChatPromptTemplate([
        ("system", system_message),
        ("human", "find the cons features from this features: {features}"),
    ])

    pro_chains = pros_prompt | model | StrOutputParser()
    cons_chains = cons_prompt | model | StrOutputParser()

    # chain = prompt | model | StrOutputParser()

    format_prompt = RunnableLambda(lambda x: prompt.format_prompt(**x))
    product = input("Review Product: ")
    chain = ( prompt | model | StrOutputParser() | RunnableParallel(pros=pro_chains, cons=cons_chains) | RunnableLambda(lambda x: StrOutputParser().parse(x['pros']+'\n'+x['cons'])))

    # chain = RunnableSequence(first=format_prompt, middle=[invoke_model], last=parse_output)

    result = chain.invoke({"input": product})
    print(result)
