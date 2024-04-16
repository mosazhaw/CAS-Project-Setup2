from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env file

import os
OPENAI_KEY = os.getenv("OPENAI_KEY")
OPENAI_MODEL = "gpt-3.5-turbo-16k"