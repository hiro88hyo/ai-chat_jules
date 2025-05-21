import unittest
from unittest.mock import patch, MagicMock
import os

# Adjust the import path if your test file is not in the same directory as gemini_client.py
# For example, if gemini_client is in a 'src' folder and tests are in 'tests' folder:
# from src.gemini_client import GeminiClient
# Assuming gemini_client.py is in the same directory for this example:
from gemini_client import GeminiClient

# How to run these tests:
# Ensure you are in the `gemini_chat_app` directory.
# Run the following command in your terminal:
# python -m unittest test_gemini_client.py

class TestGeminiClient(unittest.TestCase):

    @patch.dict(os.environ, {"GEMINI_API_KEY": "test_api_key_from_env"})
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_init_with_api_key_from_env(self, mock_configure, mock_generative_model):
        """Test GeminiClient initializes correctly with API key from environment variable."""
        client = GeminiClient()
        mock_configure.assert_called_once_with(api_key="test_api_key_from_env")
        mock_generative_model.assert_called_once_with('gemini-pro')
        self.assertIsNotNone(client.model)

    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_init_with_api_key_argument(self, mock_configure, mock_generative_model):
        """Test GeminiClient initializes correctly with API key passed as argument."""
        client = GeminiClient(api_key="test_api_key_from_arg")
        mock_configure.assert_called_once_with(api_key="test_api_key_from_arg")
        mock_generative_model.assert_called_once_with('gemini-pro')
        self.assertIsNotNone(client.model)

    @patch.dict(os.environ, {}, clear=True) # Ensure GEMINI_API_KEY is not set
    def test_init_raises_value_error_if_api_key_missing(self):
        """Test GeminiClient raises ValueError if API key is not provided or in env."""
        with self.assertRaises(ValueError) as context:
            GeminiClient()
        self.assertTrue("GEMINI_API_KEY not found" in str(context.exception))

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}) # Needs a key to init client
    @patch('google.generativeai.configure') # Mock configure as it's called in init
    def test_send_prompt_successful_response(self, mock_configure):
        """Test send_prompt returns text from a successful API call."""
        client = GeminiClient() # Initializes with fake_key

        # Mock the model and its response
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        
        # Simulate the structure of a successful response
        # Option 1: Response with parts as a list of Part objects
        mock_part = MagicMock()
        mock_part.text = "Test response text"
        mock_response.candidates = [MagicMock()]
        mock_response.candidates[0].content = MagicMock()
        mock_response.candidates[0].content.parts = [mock_part]

        # Option 2: Response with parts as an object with a text attribute (less common for current API)
        # mock_response.candidates[0].content.parts = MagicMock(text="Test response text")

        mock_model_instance.generate_content.return_value = mock_response
        client.model = mock_model_instance # Replace the actual model with our mock

        response_text = client.send_prompt("Test prompt")
        client.model.generate_content.assert_called_once_with("Test prompt")
        self.assertEqual(response_text, "Test response text")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
    @patch('google.generativeai.configure')
    def test_send_prompt_api_error(self, mock_configure):
        """Test send_prompt raises an exception if the API call fails."""
        client = GeminiClient()
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = Exception("API Error")
        client.model = mock_model_instance

        with self.assertRaises(Exception) as context:
            client.send_prompt("Test prompt")
        self.assertTrue("API call failed: API Error" in str(context.exception))

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
    @patch('google.generativeai.configure')
    def test_send_prompt_empty_response_candidates(self, mock_configure):
        """Test send_prompt handles empty candidates list from API."""
        client = GeminiClient()
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.candidates = [] # Empty candidates
        mock_model_instance.generate_content.return_value = mock_response
        client.model = mock_model_instance

        response_text = client.send_prompt("Test prompt")
        self.assertEqual(response_text, "Error: Empty or malformed response from API.")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
    @patch('google.generativeai.configure')
    def test_send_prompt_malformed_response_no_content(self, mock_configure):
        """Test send_prompt handles response with no content in candidate."""
        client = GeminiClient()
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_candidate.content = None # No content
        mock_response.candidates = [mock_candidate]
        mock_model_instance.generate_content.return_value = mock_response
        client.model = mock_model_instance

        response_text = client.send_prompt("Test prompt")
        self.assertEqual(response_text, "Error: Empty or malformed response from API.")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
    @patch('google.generativeai.configure')
    def test_send_prompt_malformed_response_no_parts(self, mock_configure):
        """Test send_prompt handles response with no parts in content."""
        client = GeminiClient()
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_candidate_content = MagicMock()
        mock_candidate_content.parts = None # No parts
        mock_candidate = MagicMock()
        mock_candidate.content = mock_candidate_content
        mock_response.candidates = [mock_candidate]
        mock_model_instance.generate_content.return_value = mock_response
        client.model = mock_model_instance

        response_text = client.send_prompt("Test prompt")
        self.assertEqual(response_text, "Error: Empty or malformed response from API.")
    
    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"})
    @patch('google.generativeai.configure')
    def test_send_prompt_malformed_response_empty_parts_list(self, mock_configure):
        """Test send_prompt handles response with empty parts list in content."""
        client = GeminiClient()
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_candidate_content = MagicMock()
        mock_candidate_content.parts = [] # Empty parts list
        mock_candidate = MagicMock()
        mock_candidate.content = mock_candidate_content
        mock_response.candidates = [mock_candidate]
        mock_model_instance.generate_content.return_value = mock_response
        client.model = mock_model_instance

        response_text = client.send_prompt("Test prompt")
        self.assertEqual(response_text, "Error: Empty or malformed response from API.")

if __name__ == '__main__':
    unittest.main()
