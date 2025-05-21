# Gemini Chat App

## Description

This is a simple web-based chat application that allows users to interact with Google's Gemini Pro large language model (or other compatible Gemini models). It uses Gradio for the user interface and the `google-generativeai` Python SDK to connect to the Gemini API. Configuration is handled via a `.env` file.

## Setup and Installation

### 1. Clone the Repository (if you haven't already)
```bash
# Example:
# git clone <repository_url>
# cd gemini_chat_app
```

### 2. Create a Virtual Environment (Recommended)

It's highly recommended to use a virtual environment to manage project dependencies.

```bash
# Navigate to the project directory (e.g., gemini_chat_app)
python3 -m venv venv

# Activate the virtual environment
# On macOS and Linux:
source venv/bin/activate
# On Windows:
# venv\\Scripts\\activate
```

*Note: We encountered issues creating a venv within the specific tool environment for this project's development, but the above are standard best practices.*

### 3. Install Dependencies

Install the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

### 4. Configure API Key and Model (using `.env` file)

The application uses a `.env` file to manage your Google Gemini API key and optionally specify the model name.

1.  **Create a `.env` file:**
    In the `gemini_chat_app` directory, copy the example file `.env.example` to a new file named `.env`.
    ```bash
    cp .env.example .env
    ```

2.  **Edit the `.env` file:**
    Open the `.env` file in a text editor and update the following variables:

    *   **`GEMINI_API_KEY`**: Replace `YOUR_API_KEY_HERE` with your actual Google Gemini API key. You can obtain an API key from [Google AI Studio](https://aistudio.google.com/app/apikey) (or your Google Cloud project).

        ```dotenv
        GEMINI_API_KEY=YOUR_ACTUAL_API_KEY_GOES_HERE
        ```

    *   **`GEMINI_MODEL_NAME`** (Optional): You can specify a Gemini model to use. If this line is commented out, removed, or the variable is not set, the application will default to `'gemini-pro'`. Examples of other models include `gemini-1.0-pro` or `gemini-1.5-flash-latest`.

        ```dotenv
        # Example: Using a specific version of gemini-pro
        # GEMINI_MODEL_NAME=gemini-1.0-pro 
        
        # Example: Using the latest flash model
        # GEMINI_MODEL_NAME=gemini-1.5-flash-latest

        # If you want the default 'gemini-pro', you can leave it as is or comment it out:
        GEMINI_MODEL_NAME=gemini-pro
        ```

    **Important:** Ensure your `.env` file is never committed to version control if it contains sensitive API keys. The `.gitignore` file in this project should already be configured to ignore `.env` files.

## Running the Application

Once the dependencies are installed and the `.env` file is configured with your `GEMINI_API_KEY`:

1.  Ensure your virtual environment is activated.
2.  Navigate to the `gemini_chat_app` directory (if you are not already there).
3.  Run the application using the following command:

    ```bash
    python app.py
    ```

4.  The application will typically launch in your web browser, or it will provide a URL (e.g., `http://127.0.0.1:7860`) that you can open in your browser to access the chat interface.

If the `GEMINI_API_KEY` is not set correctly in the `.env` file or is invalid, the application will load with an error message, and the chat input will be disabled.

---

*Alternative (less recommended): Global Environment Variables*

*While using a `.env` file is recommended for this project, the application can also pick up `GEMINI_API_KEY` and `GEMINI_MODEL_NAME` if they are set as global environment variables in your system. However, the `.env` file method takes precedence if a `.env` file exists and the variables are set within it.*
