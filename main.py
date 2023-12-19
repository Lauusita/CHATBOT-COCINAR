
from langchain.agents import agent_types, AgentExecutor, initialize_agent, Tool, AgentType
from langchain.memory import ConversationBufferWindowMemory
from langchain.chat_models import ChatOpenAI

from flask import *

app= Flask(__name__)

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")


@app.route('/api/customers', methods=['POST'])
def hola():
    response = request.get_json()
    name = response.get('data').get('name')
    phone = response.get('data').get('phone')

    def names(input=""):
        return f"el nombre es {name}"
    
    def phones(input=""):
        return f"el número de teléfono es {phone}"

    tool_name = Tool(name="name", func=names, description="Useful for when you need the name of the user or the user request it")
    
    tool_phone = Tool(name="phone", func=phones, description="Useful for when you need the phone of the user or the user request it")

    tools =[tool_name, tool_phone]
    memory = ConversationBufferWindowMemory(memory_key="chat_history", k=5, return_messages=True)
    agent = initialize_agent(
        agent=AgentType.OPENAI_FUNCTIONS,
        tools=tools,
        llm= llm,
        verbose=True,
        memory= memory,
    )
    response = agent.invoke("what is the name and the phone of the user?")
    print(response.get('output'))
    return response.get('output')

@app.route('/api/customers', methods=['POST'])
def main():
    response = request.get_json()
    name = response.get('data').get('name')


if __name__ == "__main__":
    app.run('strapi-trxe.onrender.com')