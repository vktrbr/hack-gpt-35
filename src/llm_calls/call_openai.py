from dotenv import load_dotenv
from loguru import logger
from openai import OpenAI

from src.config import LOGGER_FOLDER, OPENAI_API_KEY
from src.logger import save_response

load_dotenv()
logger.add(f"{LOGGER_FOLDER}/openai.log", rotation="10 MB")

client = OpenAI(api_key=OPENAI_API_KEY)


def call_openai(
        user_message: str,
        model: str,
        prefix: str = "",
        system_message: str = "You are a helpful assistant in the LLM Safety.",
        max_tokens: int = 1000
) -> str:
    """
    Call OpenAI API to generate a response.

    :param system_message:
    :param user_message:
    :param model:
    :param prefix:
    :param max_tokens:
    :return:
    """
    completion = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=[
            {
                "role": "system",
                "content": system_message
            },
            {"role": "user",
             "content": user_message},
        ]
    )
    save_response(
        logger,
        user_message,
        completion.choices[0].message.content,
        prefix or model
    )
    return completion.choices[0].message.content
