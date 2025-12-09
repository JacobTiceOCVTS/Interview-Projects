import gradio as gr #used for frontend, launches a very easy to use web server
import requests #used for the api calls

FASTAPI_URL = "http://127.0.0.1:8000/llm"

def query_backend(user_input):
    print(f"Recieved input: {user_input}. Sending request to FastAPI...")

    try:
        response = requests.get(FASTAPI_URL)

        response.raise_for_status()

        data = response.json()
        return data.get("answer", "Error: 'answer' key not found in response")
    
    except Exception as e:
        return f"ERROR: Could not get response from FastAPI. Details: {e}"

demo = gr.Interface(
    fn=query_backend,
    inputs=gr.Textbox(lines=2, placeholder="Type your question here..."),
    outputs="textbox",
    title="Project 1: Full-Stack Gradio Frontend Test",
    description="Interface running on port 7860, FastAPI on port 8000"
)

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)