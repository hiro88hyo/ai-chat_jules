import gradio as gr
from gemini_client import GeminiClient
import os

# Attempt to initialize GeminiClient and handle API key errors
gemini_client_instance = None
api_key_error = None

try:
    # Attempt to get the API key from environment variable for initialization check
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # This specific error message will be caught by the except block
        # and displayed in the Gradio interface.
        raise ValueError("GEMINI_API_KEY environment variable not set. Please set it to use the app.")
    gemini_client_instance = GeminiClient(api_key=api_key)
except ValueError as ve:
    api_key_error = str(ve)
except Exception as e:
    # Catch any other initialization errors
    api_key_error = f"An unexpected error occurred during Gemini Client initialization: {e}"

def chat_function(message, history):
    """
    Handles the chat interaction.
    Takes user message and chat history, returns model's response.
    If GeminiClient failed to initialize, it returns an error message.
    """
    if gemini_client_instance is None:
        # This should ideally be handled by disabling the input,
        # but returning a message is a fallback.
        return f"Error: Gemini Client not initialized. {api_key_error}"
    
    # Combine history and new message for context if desired,
    # but Gemini API handles history for conversational context with `start_chat`.
    # For a simple non-chat model, just send the message.
    # If using `gemini-pro` which is not inherently conversational via `generate_content`
    # without managing history explicitly or using `start_chat()`, we send the current message.
    # For a true chatbot feel with `generate_content`, one might need to prepend history.
    # However, `gr.ChatInterface` manages history display, and `gemini-pro` `generate_content`
    # is stateless by default for single turns.
    # For simplicity here, we're just sending the current message.
    # For a more conversational experience, gemini_client.py would need a chat session.
    try:
        response = gemini_client_instance.send_prompt(message)
        return response
    except Exception as e:
        return f"Error interacting with Gemini API: {e}"

# Create the Gradio Chat Interface
# If API key was missing, display the error and disable the input.
iface_title = "Gemini Chat App"
interface_description = "A simple chat interface to interact with Google's Gemini Pro model."

if api_key_error:
    # Display error message prominently if API key is missing or client init failed
    with gr.Blocks() as demo:
        gr.Markdown(f"# {iface_title}")
        gr.Markdown(f"## Error\n{api_key_error}")
        gr.Textbox(label="Chat Input", placeholder="Chat disabled due to initialization error.", interactive=False)
    print(f"Gradio App Error: {api_key_error}") # Also print to console
else:
    # Launch the chat interface if client initialized successfully
    demo = gr.ChatInterface(
        fn=chat_function,
        title=iface_title,
        description=interface_description,
        chatbot=gr.Chatbot(label="Gemini Chatbot"),
        textbox=gr.Textbox(placeholder="Type your message here...", label="Your Message"),
        retry_btn=None, # Hiding default buttons for cleaner interface if not needed
        undo_btn=None,
        clear_btn="Clear Chat",
    )

if __name__ == '__main__':
    # The launch command will depend on whether demo was successfully created
    if 'demo' in locals():
        print("Launching Gradio App...")
        demo.launch() # Default is share=False, inline=True in most environments
    else:
        # This case should ideally not be reached if using the Blocks() error display,
        # but as a fallback:
        print("Gradio app could not be launched due to initialization errors.")
