import aiohttp
import asyncio
from enum import StrEnum

url = "http://api:5003/"
class Enpoint(StrEnum):
    role = 'role'
    question = 'question'
    

    
def generateEndpoint(enum: Enpoint) -> str:
    return url + enum

async def ask_question(question: str):
    url = generateEndpoint(Enpoint.question)
    body = {"question": question}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=body) as response:
            json_response = await response.json()
            print(json_response)
            return json_response


        
    
