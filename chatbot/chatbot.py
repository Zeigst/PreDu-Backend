from langchain import SQLDatabase
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.llms import OpenAI
import json
from chatbot.templates import *



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
        response = agent_executor.run(PROMPT)
    except Exception as e:
        response = str(e)
        if response.startswith("Could not parse LLM output: `"):
            response = "Something went wrong. Please rephrase your question."
	
    return response

def chat_layer_1(question: str, chat_history: list) -> str:
    load_dotenv()
    os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")  

    chat_history_string = ""
    for chat_message in chat_history:
        chat_history_string += f"\n{chat_message['sender']}: {chat_message['message']}"

    PROMPT = TEMPLATE_LAYER_1.format(question=question, chat_history=chat_history_string)
    
    llm = OpenAI(temperature=0, verbose=True)
    response = llm.predict(PROMPT)
    response_json = json.loads(response)

    return response_json

  