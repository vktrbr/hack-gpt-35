import requests
from loguru import logger

from src.config import LOGGER_FOLDER, HUGGINGFACE_API_KEY, DOLPHIN_ENDPOINT
from src.logger import save_response

logger.add(f"{LOGGER_FOLDER}/dolphin.log", rotation="10 MB")

API_URL = DOLPHIN_ENDPOINT
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {HUGGINGFACE_API_KEY}",
    "Content-Type": "application/json"
}


def query(prompt: str):
    payload = {
        "inputs": prompt,
        "parameters": {
            # More can be more unstable and server die
            "max_new_tokens": 1024,
            "handle_long_generation": "hole"
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.json()[0]["generated_text"]
    except Exception as e:
        logger.error(e)
        return response.text


def call_dolphin(
        user_message: str,
        prefix: str = "",
        system_message: str = "You are Dolphin, a helpful AI assistant."
) -> str:
    """

    :param user_message:
    :param model:
    :param prefix:
    :param system_message:
    :return:
    """
    prompt = f"""
    <|im_start|>system
    {system_message}<|im_end|>
    <|im_start|>user
    {user_message}<|im_end|>
    <|im_start|>assistant
    """.strip()

    output = query(prompt)
    output = output.replace(prompt, "").strip()

    save_response(logger, user_message, output, prefix or "dolphin")

    return output
