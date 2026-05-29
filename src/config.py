import os
from dotenv import load_dotenv

load_dotenv()

if not os.environ.get("OPENAI_API_KEY"):
    raise ValueError(
        "OPENAI_API_KEY is not set. Please ensure you have a .env file in the "
        "root directory with your API key, or set it in your environment variables."
    )