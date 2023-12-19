
import requests
from vertexai.preview.generative_models import GenerativeModel, Part, FunctionDeclaration, Tool
import vertexai


def post_info(name, email, phone):
    data = requests.post('https://strapi-trxe.onrender.com/api/customers',json={
    "data":{
        "name": name,
        "phone": phone,
        "email": email
    }
    }) 
    return data.text

def get_info(introduction):
    
    info = requests.get('https://strapi-trxe.onrender.com/api/courses').text
    return info

tools = Tool(function_declarations=[
    FunctionDeclaration(
        name="post_info", 
        description="Sube al API la información solicitada",
        parameters={"type": "object", "properties": 
                        {"name": {"type": "string", "description": "the name of the user, you will save it on 'name': name and when you have email and phone, post it"},
                        "email": {"type": "string", "description": "the email of the user, you will save it on 'email': email and when you have name and phone, post it"},
                        "phone": {"type": "number", "description": "the number phone of the user, you will save it on 'phone': phone and when you have email and name, post it"}
                        }
                    }
    ),
    FunctionDeclaration(
        name="get_info", 
        description="Obtiene los nombres de y la descripción de los cursos",
        parameters={"type": "object", "properties": {"info": {"type": "string", "description": "the data of each course"}}}
        )
])

vertexai.init(project="elena-ai-dev")
model = GenerativeModel('gemini-pro', generation_config={"temperature": 0.2}, tools=[tools])

chat = model.start_chat()

prompt = "Mi nombre es Ludmila, email Ludmila@gmail.com y número 35895234738"
response = chat.send_message(prompt)

function_call = response.candidates[0].content.parts[0].function_call
function_handlebars = {
    "get_info": get_info,
    "post_info": post_info
}

if function_call.name in function_handlebars:
    function_name = function_call.name

    args = {key: value for key, value in function_call.args.items()}

    function_response = function_handlebars[function_name](**args)

    print(function_response)
    response = chat.send_message(Part.from_function_response(name=function_name, response={"content": function_response}))
    print(response)
    print(response.candidates[0].content.parts[0].text)
else:
    print( "hola")