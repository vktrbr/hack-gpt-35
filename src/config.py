import os

from dotenv import load_dotenv

load_dotenv()

REQ_FOLDER = os.getenv("REQ_FOLDER")
FINETUNE_FOLDER = os.getenv("FINETUNE_FOLDER")
LOGGER_FOLDER = os.getenv("LOGGER_FOLDER")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")

DOLPHIN_ENDPOINT = os.getenv("DOLPHIN_ENDPOINT")
INAPPROPRIATE_ENDPOINT = os.getenv("INAPPROPRIATE_ENDPOINT")
OPENAI_FOLDER_RESULTS = os.getenv("OPENAI_FOLDER_RESULTS")
