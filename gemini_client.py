import os
import google.generativeai as genai

class GeminiClient:
    """
    A client for interacting with the Google Gemini API.
    The API key and model name can be provided as arguments or loaded from 
    environment variables (GEMINI_API_KEY, GEMINI_MODEL_NAME).
    """
    def __init__(self, api_key: str = None, model_name: str = None):
        """
        Initializes the GeminiClient.

        The API key is determined in the following order of precedence:
        1. api_key argument.
        2. GEMINI_API_KEY environment variable.

        The model name is determined in the following order of precedence:
        1. model_name argument.
        2. GEMINI_MODEL_NAME environment variable.
        3. Default value: 'gemini-pro'.

        Args:
            api_key (str, optional): The API key for Gemini. Defaults to None.
            model_name (str, optional): The name of the Gemini model to use. 
                                        Defaults to None (which then defaults to 'gemini-pro' 
                                        if not set in environment).

        Raises:
            ValueError: If the API key is not provided as an argument and not found 
                        in the GEMINI_API_KEY environment variable.
        """
        # Determine API key
        if api_key is None:
            api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("API key not provided or found in environment variables.")

        genai.configure(api_key=api_key)

        # Determine model name
        if model_name is None:
            model_name = os.environ.get("GEMINI_MODEL_NAME")
        
        if model_name is None:
            self.model_name = 'gemini-pro' # Default model
        else:
            self.model_name = model_name
            
        self.model = genai.GenerativeModel(self.model_name)
        print(f"GeminiClient initialized with model: {self.model_name}") # For verification

    def send_prompt(self, prompt: str) -> str:
        """
        Sends a prompt to the configured Gemini model and returns the text response.

        Args:
            prompt (str): The prompt to send to the API.

        Returns:
            str: The text response from the API.

        Raises:
            Exception: If there's an error during the API call or if the response is malformed.
        """
        try:
            response = self.model.generate_content(prompt)
            # More robust response parsing
            if response and response.candidates:
                first_candidate = response.candidates[0]
                if first_candidate.content and first_candidate.content.parts:
                    if isinstance(first_candidate.content.parts, list) and len(first_candidate.content.parts) > 0:
                        return first_candidate.content.parts[0].text
                    # Fallback for older/different structures if parts is not a list but has text
                    elif hasattr(first_candidate.content.parts, 'text'): 
                        return first_candidate.content.parts.text
            
            # If the structure is not as expected or parts are empty
            error_message = "Error: Empty or malformed response from API."
            print(f"send_prompt issue: {error_message} - Response: {response}")
            return error_message
            
        except Exception as e:
            print(f"An error occurred in send_prompt: {e}")
            raise Exception(f"API call failed using model {self.model_name}: {e}")

if __name__ == '__main__':
    # Example usage:
    # Ensure .env file is loaded by the main application if running this directly,
    # or set environment variables manually for testing this script.
    print("Running GeminiClient example...")
    
    # To test model_name from env: export GEMINI_MODEL_NAME="your-model"
    # To test api_key from env: export GEMINI_API_KEY="your-api-key"

    try:
        # Test case 1: API key from env, default model
        # Ensure GEMINI_API_KEY is set in your environment for this to pass
        if os.getenv("GEMINI_API_KEY"):
            print("\n--- Test Case 1: API key from env, default model ---")
            client_env_key = GeminiClient()
            prompt1 = "Tell me a fun fact about the Python programming language."
            print(f"Sending prompt to {client_env_key.model_name}: {prompt1}")
            response1 = client_env_key.send_prompt(prompt1)
            print(f"Gemini's response: {response1}\n")
        else:
            print("\nSkipping Test Case 1: GEMINI_API_KEY not set in environment.")

        # Test case 2: API key as argument, specific model name as argument
        # Replace "YOUR_ACTUAL_API_KEY" with a valid key if you want to run this live.
        # For non-live test, it will fail at configure/generate_content if key is invalid.
        # For now, we are mostly testing initialization logic.
        print("\n--- Test Case 2: API key as argument, model name as argument ---")
        # Use a placeholder key for init testing if a real one isn't easily available for test env
        test_api_key_arg = os.getenv("GEMINI_API_KEY", "placeholder_api_key_for_init_test")
        custom_model = "gemini-pro" # or your specific model if different and key is valid
        client_args = GeminiClient(api_key=test_api_key_arg, model_name=custom_model)
        prompt2 = "What is the difference between Python lists and tuples?"
        print(f"Sending prompt to {client_args.model_name}: {prompt2}")
        # The following line will only work if test_api_key_arg is a valid key
        # and custom_model is a valid model for that key.
        if test_api_key_arg != "placeholder_api_key_for_init_test":
             response2 = client_args.send_prompt(prompt2)
             print(f"Gemini's response: {response2}\n")
        else:
            print("Skipping actual prompt sending for Test Case 2 due to placeholder API key.")
            print(f"Client initialized with model: {client_args.model_name} and a placeholder key.")


        # Test case 3: API key from env, model_name from env
        if os.getenv("GEMINI_API_KEY") and os.getenv("GEMINI_MODEL_NAME"):
            print("\n--- Test Case 3: API key from env, model_name from env ---")
            client_env_model = GeminiClient() # Will pick up both from env
            prompt3 = "Explain quantum computing in simple terms."
            print(f"Sending prompt to {client_env_model.model_name}: {prompt3}")
            response3 = client_env_model.send_prompt(prompt3)
            print(f"Gemini's response: {response3}\n")
        else:
            print("\nSkipping Test Case 3: GEMINI_API_KEY or GEMINI_MODEL_NAME not set in environment.")

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as ex:
        print(f"Runtime Error: {ex}")
