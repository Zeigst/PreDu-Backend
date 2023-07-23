from database import create_session
from models import *

session = create_session()


from langchain import SQLDatabase
import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit

from langchain.llms import OpenAI
import json

from chatbot.chatbot import chat_layer_1, chat_layer_2

# response = chat_layer_1("Introduce yourself and tell me about the shop")
# print(response)

chat_history_string = ""
chat_history_string += "asfghg"
print(chat_history_string)

