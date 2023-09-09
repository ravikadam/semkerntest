from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.templating import Jinja2Templates
import requests
from bs4 import BeautifulSoup
import semantic_kernel as sk
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion
import asyncio



kernel = sk.Kernel()
api_key, org_id = sk.openai_settings_from_dot_env()

kernel.add_chat_service("chat-gpt", OpenAIChatCompletion("gpt-3.5-turbo", api_key, org_id))


app = FastAPI()

templates = Jinja2Templates(directory="templates")

async def semantic_kernel(url: str) -> str:
    # ... [rest of the semantic_kernel function]
        try:
            response = requests.get(url)
            response.raise_for_status()
    
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs = soup.find_all('p')
            text = ' '.join(para.text for para in paragraphs)
    
            # For now, we'll return the first 300 characters as a summary.
            # In a real-world scenario, you'd use a more sophisticated method.

            skill = kernel.import_semantic_skill_from_directory("./skills","raviskills")
            sum_function = skill["summary"]

            result =  await kernel.run_async(sum_function, input_str=text)
            
            return str(result) + "..."
        except requests.RequestException:
            raise HTTPException(status_code=400, detail="Error fetching the URL")

@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/generate-summary/")
async def generate_summary(request: Request, url: str = Form(...)):
    summary =  await semantic_kernel(url)
    return templates.TemplateResponse("index.html", {"request": request, "summary": summary})

