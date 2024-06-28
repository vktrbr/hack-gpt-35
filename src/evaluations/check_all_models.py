import pandas as pd
from loguru import logger

from src.config import FINETUNE_FOLDER, OPENAI_FOLDER_RESULTS, LOGGER_FOLDER
from src.llm_calls.call_llama_guard import check_inappropriate

logger.add(f"{LOGGER_FOLDER}/check_all_models.log", rotation="10 MB")

dataset = pd.read_csv(f"{FINETUNE_FOLDER}/train-105-examples-w-ids.csv")
dataset_gpt = pd.read_csv(
    f"{OPENAI_FOLDER_RESULTS}/results-gpt-3.5-turbo-1106.csv")
dataset_ft_gpt = pd.read_csv(
    f"{OPENAI_FOLDER_RESULTS}/results-ft-gpt-3.5-turbo-1106-9es06jue.csv")

results = []

for index, row in dataset.iterrows():
    uuid = row["uuid"]

    result_dolphin = check_inappropriate(
        row["request"],
        row["response"]
    )

    result_gpt35 = check_inappropriate(
        row["request"],
        dataset_gpt[dataset_gpt.uuid_request == uuid].iloc[0]["response"]
    )

    result_ft_gpt35 = check_inappropriate(
        row["request"],
        dataset_ft_gpt[dataset_ft_gpt.uuid_request == uuid].iloc[0]["response"]
    )

    results.append({
        "uuid": uuid,
        "dolphin_safety": result_dolphin["result"],
        "dolphin_violations": result_dolphin["violated_categories"],
        "gpt35_safety": result_gpt35["result"],
        "gpt35_violations": result_gpt35["violated_categories"],
        "ft_gpt35_safety": result_ft_gpt35["result"],
        "ft_gpt35_violations": result_ft_gpt35["violated_categories"]
    })

    logger.info(f"Request {uuid} done {index}/{len(dataset)}")

df = pd.DataFrame(results)
df.to_csv(f"{OPENAI_FOLDER_RESULTS}/results-check-all-models-v2.csv",
          index=False)

logger.info("All requests done")
