from database import create_session
from models import *
import os
from dotenv import load_dotenv

from chatbot.templates import *

from langchain.llms import OpenAI
from langchain import PromptTemplate
from langchain.chains import LLMChain
import asyncio

session = create_session()

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

    response = await chain.arun(question="hi", chat_history="AI: Hi there! I'm PreDu ChatBot, here to help you with any questions you may have about PreDu. Is there anything I can help you with?")
    return response

async def main():
    response = await chat_layer_1("", [])
    print(response)

# Run the asynchronous function using asyncio
if __name__ == "__main__":
    asyncio.run(main())

