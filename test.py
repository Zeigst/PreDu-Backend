from database import create_session
from models import *
import os
from dotenv import load_dotenv

from chatbot.templates import *

from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import asyncio
from chatbot.chatbot import *
session = create_session()

response = chat_layer_2("My order cost 200.000 VND. Please give me a coupoon to use on my order.", [])
print(response) 

