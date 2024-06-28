import json
from datetime import datetime

from src.config import REQ_FOLDER


def save_response(logger, request, output, prefix: str = ''):
    logger.info(f"{request} -> %%%\n{output}\n%%%")

    hk = datetime.now().isoformat(timespec='seconds').replace(':', '-')
    prefix = prefix + "-" if prefix else ""
    with open(f"{REQ_FOLDER}/{prefix}{hk}.json", 'w') as f:
        json.dump({
            "request": request,
            "response": output
        },
            f, indent=4, ensure_ascii=False)
