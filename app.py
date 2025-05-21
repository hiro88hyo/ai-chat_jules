import gradio as gr
from gemini_client import GeminiClient
import os
from dotenv import load_dotenv

# Load environment variables from .env file at the very beginning
load_dotenv()

# Attempt to initialize GeminiClient and handle API key errors
# GeminiClient will now use os.getenv internally, which will have .env variables if loaded.
gemini_client_instance = None
api_key_error_message = None # Renamed for clarity from api_key_error

try:
    # No need to manually getenv here for api_key for GeminiClient instantiation,
    # GeminiClient's __init__ handles that.
    # We only call GeminiClient() and it will raise ValueError if key is ultimately not found.
    gemini_client_instance = GeminiClient() 
except ValueError as ve:
    api_key_error_message = str(ve)
except Exception as e:
    # Catch any other unexpected errors during GeminiClient initialization
    api_key_error_message = f"An unexpected error occurred during Gemini Client initialization: {e}"

def chat_function(message, history):
    """
    Handles the chat interaction.
    Takes user message and chat history, returns model's response.
    If GeminiClient failed to initialize, it returns an error message.
    """
    if gemini_client_instance is None:
        # This state means GeminiClient failed to initialize.
        # api_key_error_message should contain the reason.
        return f"Error: Gemini Client not initialized. {api_key_error_message}"
    
    try:
        response = gemini_client_instance.send_prompt(message)
        return response
    except Exception as e:
        return f"Error interacting with Gemini API: {e}"

# Create the Gradio Chat Interface
iface_title = "Gemini Chat App"
interface_description = "A simple chat interface to interact with Google's Gemini Pro model."
interface_description += "\nEnsure your GEMINI_API_KEY (and optional GEMINI_MODEL_NAME) are set in a .env file or your environment."


if api_key_error_message:
    # Display error message prominently if API key is missing or client init failed
    with gr.Blocks() as demo:
        gr.Markdown(f"# {iface_title}")
        gr.Markdown(f"## Initialization Error\n{api_key_error_message}")
        gr.Markdown("Please ensure your `GEMINI_API_KEY` is correctly set in a `.env` file in the application's root directory or as an environment variable.")
        gr.Textbox(label="Chat Input", placeholder="Chat disabled due to initialization error.", interactive=False)
    print(f"Gradio App Initialization Error: {api_key_error_message}") # Also print to console
else:
    # Launch the chat interface if client initialized successfully
    demo = gr.ChatInterface(
        fn=chat_function,
        title=iface_title,
        description=interface_description,
        chatbot=gr.Chatbot(label=f"Gemini Chatbot ({gemini_client_instance.model_name if gemini_client_instance else 'model_unknown'})"),
        textbox=gr.Textbox(placeholder="Type your message here...", label="Your Message"),
        retry_btn=None, 
        undo_btn=None,
        clear_btn="Clear Chat",
    )

if __name__ == '__main__':
    if 'demo' in locals() and demo is not None:
        print("Launching Gradio App...")
        # To allow external access if needed, set server_name="0.0.0.0"
        # demo.launch(server_name="0.0.0.0") # Example for broader network access
        demo.launch() 
    else:
        print("Gradio app could not be launched due to initialization errors. Check console for messages.")
