import os
import openai
import logging
from dotenv import load_dotenv

ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")


def is_openai_key_valid():
    openai.api_key = api_key
    try:
        openai.models.list()  # This retrieves the list of available models
        return True
    except Exception as e:
        logging.error(f"An error occurred while validating the API key: {e}")
        return False
