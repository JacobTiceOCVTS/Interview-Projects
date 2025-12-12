#Jacob Tice OCVTS - Interview Project 1
#I will be using comments as my notes

from fastapi import FastAPI #fastAPI will be used for the main logic
import ollama #can be used to run LLM's
from fastapi.responses import JSONResponse

app = FastAPI() #creates an instance of the web appliciation

@app.get("/") #makes it so the following function responds when a GET request is sent to the root URL of the http server
def read_root():
    return {"message": "Hello from backend"}


@app.get("/llm") #new endpoint for the API request
def llm_test(user_prompt: str):
    print(f"Prompt from frontend recieved: {user_prompt}")
    try:
        #generates a repsonse using ollama, via deepseek model
        #returns the response as an object
        response = ollama.generate(
            model='gemma3:12b',
            prompt=user_prompt,
        )
        print({"answer": response['response']})
        return {"answer": response['response']}#response is a dictionary and the reponse key is just the text the AI will respond withokay
    except Exception as e:
        
        return JSONResponse(
            status_code=500,
            content={
                "error": "Ollama Connection Failed",
                "detail": f"Could not connect to the AI Model. Is the ollama service running? Error: {e}"
            }
            )