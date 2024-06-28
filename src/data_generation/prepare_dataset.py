import json
import os

import pandas as pd
from loguru import logger

from src.config import REQ_FOLDER, FINETUNE_FOLDER, LOGGER_FOLDER

logger.add(
    os.path.join(LOGGER_FOLDER, "prepare_dataset.log"),
    rotation="10 MB"
)

list_of_files = os.listdir(REQ_FOLDER)
len_files = len(list_of_files)
logger.info(f"Number of files: {len_files}")

SYSTEM = "You are GPT35, a helpful AI assistant."
dataset = []

for i in range(len_files):
    if not list_of_files[i].endswith(".json"):
        continue
    file_path = os.path.join(REQ_FOLDER, list_of_files[i])

    logger.info(f"Processing file: {list_of_files[i]}")
    topic_tags = list_of_files[i].split("2024")[0].split("-")
    version = topic_tags[2]
    theme = topic_tags[3]
    theme_request = topic_tags[4]
    short_description = " ".join(topic_tags[5:])

    idx = str(hex(hash(list_of_files[i])))[-8:]

    with open(file_path) as f:
        data = json.load(f)

        example = {
            "messages": [
                {"role": "system", "content": SYSTEM},
                {"role": "user", "content": data["request"].strip()},
                {"role": "assistant", "content": data["response"].strip()}
            ]
        }
        with open(
                os.path.join(FINETUNE_FOLDER,
                             f"train-{len_files}-examples.jsonl"),
                mode="a"
        ) as jsonl:
            jsonl.write(json.dumps(example, ensure_ascii=False) + "\n")

        dataset.append({
            "uuid": idx,
            "version": version,
            "theme": theme,
            "theme_request": theme_request,
            "short_description": short_description,
            "request": data["request"].strip(),
            "response": data["response"].strip()
        })
        logger.info(f"Processed file {i + 1}/{len_files}")

dataset = pd.DataFrame(dataset)
dataset.to_csv(
    os.path.join(FINETUNE_FOLDER,
                 f"train-{len_files}-examples-w-ids.csv"),
    index=False
)
