import gradio as gr #used for frontend, launches a very easy to use web server
import requests #used for the api calls

FASTAPI_URL = "http://127.0.0.1:8000/llm" #url endpoint for the llm

#function sends the query to the fastapi backend and returns response or error
def query_backend(user_input):
    #status message announcing what the program is doing
    print(f"Recieved input: {user_input}. Sending request to FastAPI...")

    #trys getting the api response, turning it into json, then returning the answer
    try:
        response = requests.get(FASTAPI_URL, params={"user_prompt":user_input})

        response.raise_for_status()

        data = response.json()
        return data.get("answer", "Error: 'answer' key not found in response")
    
    #returns error if this process fails at any point
    except Exception as e:
        return f"ERROR: Could not get response from FastAPI. Details: {e}"

#sets up the demo with 2 text boxes for I/O, some description, and the function to use
demo = gr.Interface(
    fn=query_backend,
    inputs=gr.Textbox(lines=2, placeholder="Type your question here..."),
    outputs=gr.Textbox(lines=20, label="Response from LLM"),
    title="Project 1: Full-Stack Gradio Frontend Test",
    description="Interface running on port 7860, FastAPI on port 8000"
)

#runs the demo on a different port than the backend
demo.launch(server_name="0.0.0.0", server_port=7860)