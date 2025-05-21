import os
import google.generativeai as genai

class GeminiClient:
    """
    A client for interacting with the Google Gemini API.
    The API key is expected to be set in the GEMINI_API_KEY environment variable.
    """
    def __init__(self, api_key: str = None):
        """
        Initializes the GeminiClient.

        Args:
            api_key (str, optional): The API key for Gemini. 
                                     If None, it attempts to load from 
                                     the GEMINI_API_KEY environment variable.

        Raises:
            ValueError: If the API key is not provided and not found in environment variables.
        """
        if api_key is None:
            api_key = os.getenv("GEMINI_API_KEY")
        
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found. Please set the environment variable or pass the api_key argument.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def send_prompt(self, prompt: str) -> str:
        """
        Sends a prompt to the Gemini API and returns the text response.

        Args:
            prompt (str): The prompt to send to the API.

        Returns:
            str: The text response from the API.

        Raises:
            Exception: If there's an error during the API call.
        """
        try:
            response = self.model.generate_content(prompt)
            # Ensure that the response and its parts are not None before accessing text
            if response and response.candidates and response.candidates[0].content and response.candidates[0].content.parts:
                 # Check if parts is a list and not empty
                if isinstance(response.candidates[0].content.parts, list) and len(response.candidates[0].content.parts) > 0:
                    return response.candidates[0].content.parts[0].text
                # Check if parts is an object with a text attribute (for older versions or different response structures)
                elif hasattr(response.candidates[0].content.parts, 'text'):
                     return response.candidates[0].content.parts.text
            return "Error: Empty or malformed response from API."
        except Exception as e:
            # Log the exception or handle it more gracefully
            print(f"An error occurred: {e}")
            # Raise a custom exception or return an error message
            raise Exception(f"API call failed: {e}")

if __name__ == '__main__':
    # Example usage (requires GEMINI_API_KEY to be set)
    try:
        client = GeminiClient()
        sample_prompt = "Hello Gemini! What can you do?"
        print(f"Sending prompt: {sample_prompt}")
        response_text = client.send_prompt(sample_prompt)
        print(f"Gemini's response: {response_text}")
    except ValueError as ve:
        print(ve)
    except Exception as ex:
        print(ex)
