import os

import pandas as pd
from loguru import logger

from src.config import FINETUNE_FOLDER, OPENAI_FOLDER_RESULTS
from src.config import LOGGER_FOLDER
from src.llm_calls.call_openai import call_openai

logger.add(os.path.join(LOGGER_FOLDER, "check_gpt35.log"), rotation="10 MB")


def check_gpt35(
        model: str,
        output_path: str,
        file_path: str = f"{FINETUNE_FOLDER}/train-105-examples-w-ids.csv",
        max_tokens: int = 1000
) -> str:
    """
    Check the GPT-3.5 model for the same dataset but different models
    
    :param model:
    :param output_path:
    :param file_path:
    :param max_tokens:
    :return: 
    """
    dataset = pd.read_csv(file_path)
    logger.info(f"Columns: {', '.join(dataset.columns)}")

    assert model in [
        "gpt-3.5-turbo-1106",
        "ft:gpt-3.5-turbo-1106:personal:itmo-hack-project:9es06jue"
    ], f"Model {model} not supported"

    results = []

    for index, row in dataset.iterrows():
        request = row["request"]
        logger.info(f"Checking request: {index} - {row['uuid']}")
        response = call_openai(
            request,
            model=model,
            prefix=f"test-harmful-{model}",
            system_message="",
            max_tokens=max_tokens
        )
        results.append(
            {
                "uuid_request": row["uuid"],
                "uuid_response": str(hex(hash(response)))[-8:],
                "response": response
            }
        )

    results_df = pd.DataFrame(results)
    results_df.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    # check_gpt35(
    #     "gpt-3.5-turbo-1106",
    #     f"{OPENAI_FOLDER_RESULTS}/results-gpt-3.5-turbo-1106.csv"
    # )

    check_gpt35(
        "ft:gpt-3.5-turbo-1106:personal:itmo-hack-project:9es06jue",
        f"{OPENAI_FOLDER_RESULTS}/results-ft-gpt-3.5-turbo-1106-9es06jue.csv",
        max_tokens=1024
    )
