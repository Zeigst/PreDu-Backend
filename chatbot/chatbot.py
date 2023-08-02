from langchain import SQLDatabase
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.llms import OpenAI
import json
from chatbot.templates import *
from langchain.chains import LLMChain
from langchain import PromptTemplate
import asyncio



def chat_layer_2(question: str, chat_history: list) -> str:
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

    chat_history_string = ""
    for chat_message in chat_history:
        chat_history_string += f"\n{chat_message['sender']}: {chat_message['message']}"

    PROMPT = TEMPLATE_LAYER_2.format(question=question, chat_history=chat_history_string)

    db = SQLDatabase.from_uri(os.getenv("DB_URL"), 
        include_tables=[ 'categories', 'brands', 'products', 'coupons'],
        sample_rows_in_table_info=2)
    
    llm = ChatOpenAI(
        model_name = "gpt-3.5-turbo",  
        temperature=0.3, 
        verbose=True,
        openai_api_key=os.getenv("OPENAI_API_KEY"))

    toolkit = SQLDatabaseToolkit(db=db, llm=llm)

    agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        verbose=True
    )

    try:
        response =  agent_executor.run(PROMPT)
    except Exception as e:
        response = str(e)
        if response.startswith("Could not parse LLM output: `"):
            prefix = "Could not parse LLM output: `"
            response = response[len(prefix):]
    
    return response

async def chat_layer_2_async_wrapper(question: str, chat_history: list) -> str:
    loop = asyncio.get_event_loop()
    response = await loop.run_in_executor(None, chat_layer_2, question, chat_history)
    # response = asyncio.to_thread(chat_layer_2, question, chat_history)
    return response

async def chat_layer_1(question: str, chat_history: list) -> str:
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  

    chat_history_string = ""
    for chat_message in chat_history:
        chat_history_string += f"\n{chat_message['sender']}: {chat_message['message']}"

    
    llm = OpenAI(temperature=0)
    prompt = PromptTemplate(
        input_variables=["question", "chat_history"],
        template=TEMPLATE_LAYER_1
    )
    
    chain = LLMChain(llm=llm, prompt=prompt)
    
    
    response = await chain.arun(question=question, chat_history=chat_history_string)
    response_json = json.loads(response)

    return response_json

  