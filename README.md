# Gemini Chat App

## Description

This is a simple web-based chat application that allows users to interact with Google's Gemini Pro large language model. It uses Gradio for the user interface and the `google-generativeai` Python SDK to connect to the Gemini API.

## Setup and Installation

### 1. Create a Virtual Environment (Recommended)

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create a virtual environment (e.g., named 'venv')
python3 -m venv venv

# Activate the virtual environment
# On macOS and Linux:
source venv/bin/activate
# On Windows:
# venv\\Scripts\\activate
```

*Note: We encountered issues creating a venv within the specific tool environment for this project's development, but the above are standard best practices.*

### 2. Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 3. Set the GEMINI_API_KEY Environment Variable

To use this application, you need a Google Gemini API key. 

1.  Obtain an API key from [Google AI Studio](https://aistudio.google.com/app/apikey) (or your Google Cloud project).
2.  Set it as an environment variable named `GEMINI_API_KEY`.

   **On macOS and Linux:**
   ```bash
   export GEMINI_API_KEY="YOUR_API_KEY_HERE"
   ```
   You might want to add this line to your shell's configuration file (e.g., `~/.bashrc`, `~/.zshrc`) for persistence across sessions.

   **On Windows (Command Prompt):**
   ```bash
   set GEMINI_API_KEY=YOUR_API_KEY_HERE
   ```
   **On Windows (PowerShell):**
   ```bash
   $env:GEMINI_API_KEY="YOUR_API_KEY_HERE"
   ```
   For persistent storage on Windows, search for "environment variables" in the system settings.

## Running the Application

Once the dependencies are installed and the `GEMINI_API_KEY` is set:

1.  Navigate to the `gemini_chat_app` directory (if you are not already there).
2.  Run the application using the following command:

    ```bash
    python app.py
    ```

3.  The application will typically launch in your web browser, or it will provide a URL (e.g., `http://127.0.0.1:7860`) that you can open in your browser to access the chat interface.

If the `GEMINI_API_KEY` is not set or is invalid, the application will load with an error message and the chat input will be disabled.
