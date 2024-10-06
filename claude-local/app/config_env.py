import os

from dotenv import load_dotenv


def config_env() -> str | None:
    """Loads the api key from the .env file."""
    load_dotenv()
    api_key = os.getenv("API_KEY")
    return api_key
