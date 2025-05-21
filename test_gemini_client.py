import unittest
from unittest.mock import patch, MagicMock
import os

# Assuming gemini_client.py is in the same directory for this example:
from gemini_client import GeminiClient

# How to run these tests:
# Ensure you are in the `gemini_chat_app` directory.
# Run the following command in your terminal:
# python -m unittest test_gemini_client.py

class TestGeminiClient(unittest.TestCase):

    # --- API Key Initialization Tests ---
    @patch.dict(os.environ, {"GEMINI_API_KEY": "env_api_key"}, clear=True)
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_init_api_key_from_env_primary(self, mock_configure, mock_generative_model):
        """Test GeminiClient uses API key from environment if no argument is passed."""
        client = GeminiClient()
        mock_configure.assert_called_once_with(api_key="env_api_key")
        self.assertEqual(client.model_name, 'gemini-pro') # Default model
        mock_generative_model.assert_called_once_with('gemini-pro')
        self.assertIsNotNone(client.model)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "env_api_key"}, clear=True)
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_init_api_key_from_argument_overrides_env(self, mock_configure, mock_generative_model):
        """Test GeminiClient uses API key from argument even if env var is set."""
        client = GeminiClient(api_key="arg_api_key")
        mock_configure.assert_called_once_with(api_key="arg_api_key")
        self.assertEqual(client.model_name, 'gemini-pro') # Default model
        mock_generative_model.assert_called_once_with('gemini-pro')
        self.assertIsNotNone(client.model)

    @patch.dict(os.environ, {}, clear=True) # Ensure GEMINI_API_KEY is not set
    def test_init_raises_value_error_if_api_key_missing_altogether(self):
        """Test GeminiClient raises ValueError if API key is not in arg or env."""
        with self.assertRaises(ValueError) as context:
            GeminiClient()
        self.assertTrue("API key not provided or found in environment variables." in str(context.exception))

    # --- Model Name Initialization Tests ---
    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key", "GEMINI_MODEL_NAME": "env_model_name"}, clear=True)
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_init_model_name_from_env(self, mock_configure, mock_generative_model):
        """Test GeminiClient uses model name from GEMINI_MODEL_NAME env var."""
        client = GeminiClient() # API key from env
        mock_configure.assert_called_once_with(api_key="fake_key")
        self.assertEqual(client.model_name, "env_model_name")
        mock_generative_model.assert_called_once_with("env_model_name")
        self.assertIsNotNone(client.model)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key", "GEMINI_MODEL_NAME": "env_model_name"}, clear=True)
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_init_model_name_from_argument_overrides_env(self, mock_configure, mock_generative_model):
        """Test model_name argument overrides GEMINI_MODEL_NAME env var."""
        client = GeminiClient(model_name="arg_model_name") # API key from env
        mock_configure.assert_called_once_with(api_key="fake_key")
        self.assertEqual(client.model_name, "arg_model_name")
        mock_generative_model.assert_called_once_with("arg_model_name")
        self.assertIsNotNone(client.model)

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key"}, clear=True) # GEMINI_MODEL_NAME is not set
    @patch('google.generativeai.GenerativeModel')
    @patch('google.generativeai.configure')
    def test_init_model_name_defaults_if_not_in_arg_or_env(self, mock_configure, mock_generative_model):
        """Test GeminiClient defaults model to 'gemini-pro' if not in arg or env."""
        client = GeminiClient() # API key from env
        mock_configure.assert_called_once_with(api_key="fake_key")
        self.assertEqual(client.model_name, 'gemini-pro')
        mock_generative_model.assert_called_once_with('gemini-pro')
        self.assertIsNotNone(client.model)

    # --- Send Prompt Tests (remain largely the same, ensure API key for init) ---
    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_for_prompt_tests"}, clear=True)
    @patch('google.generativeai.configure') # Mock configure as it's called in init
    def test_send_prompt_successful_response(self, mock_configure):
        """Test send_prompt returns text from a successful API call."""
        client = GeminiClient() # Initializes with fake_key_for_prompt_tests and default model

        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_part = MagicMock()
        mock_part.text = "Test response text"
        mock_response.candidates = [MagicMock(content=MagicMock(parts=[mock_part]))]
        
        mock_model_instance.generate_content.return_value = mock_response
        client.model = mock_model_instance 

        response_text = client.send_prompt("Test prompt")
        client.model.generate_content.assert_called_once_with("Test prompt")
        self.assertEqual(response_text, "Test response text")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_for_error_tests"}, clear=True)
    @patch('google.generativeai.configure')
    def test_send_prompt_api_error(self, mock_configure):
        """Test send_prompt raises an exception if the API call fails."""
        client = GeminiClient()
        
        mock_model_instance = MagicMock()
        mock_model_instance.generate_content.side_effect = Exception("API Error")
        client.model = mock_model_instance

        with self.assertRaises(Exception) as context:
            client.send_prompt("Test prompt")
        self.assertTrue(f"API call failed using model {client.model_name}: API Error" in str(context.exception))

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_for_malformed_tests"}, clear=True)
    @patch('google.generativeai.configure')
    def test_send_prompt_empty_response_candidates(self, mock_configure):
        """Test send_prompt handles empty candidates list from API."""
        client = GeminiClient()
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_response.candidates = [] 
        mock_model_instance.generate_content.return_value = mock_response
        client.model = mock_model_instance

        response_text = client.send_prompt("Test prompt")
        self.assertEqual(response_text, "Error: Empty or malformed response from API.")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_for_malformed_tests"}, clear=True)
    @patch('google.generativeai.configure')
    def test_send_prompt_malformed_response_no_content(self, mock_configure):
        """Test send_prompt handles response with no content in candidate."""
        client = GeminiClient()
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_candidate = MagicMock()
        mock_candidate.content = None 
        mock_response.candidates = [mock_candidate]
        mock_model_instance.generate_content.return_value = mock_response
        client.model = mock_model_instance

        response_text = client.send_prompt("Test prompt")
        self.assertEqual(response_text, "Error: Empty or malformed response from API.")

    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_for_malformed_tests"}, clear=True)
    @patch('google.generativeai.configure')
    def test_send_prompt_malformed_response_no_parts(self, mock_configure):
        """Test send_prompt handles response with no parts in content."""
        client = GeminiClient()
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_candidate_content = MagicMock()
        mock_candidate_content.parts = None 
        mock_candidate = MagicMock(content=mock_candidate_content)
        mock_response.candidates = [mock_candidate]
        mock_model_instance.generate_content.return_value = mock_response
        client.model = mock_model_instance

        response_text = client.send_prompt("Test prompt")
        self.assertEqual(response_text, "Error: Empty or malformed response from API.")
    
    @patch.dict(os.environ, {"GEMINI_API_KEY": "fake_key_for_malformed_tests"}, clear=True)
    @patch('google.generativeai.configure')
    def test_send_prompt_malformed_response_empty_parts_list(self, mock_configure):
        """Test send_prompt handles response with empty parts list in content."""
        client = GeminiClient()
        mock_model_instance = MagicMock()
        mock_response = MagicMock()
        mock_candidate_content = MagicMock()
        mock_candidate_content.parts = [] # Empty parts list
        mock_candidate = MagicMock(content=mock_candidate_content)
        mock_response.candidates = [mock_candidate]
        mock_model_instance.generate_content.return_value = mock_response
        client.model = mock_model_instance

        response_text = client.send_prompt("Test prompt")
        self.assertEqual(response_text, "Error: Empty or malformed response from API.")

if __name__ == '__main__':
    unittest.main()
