import os
from typing import List, Dict


class Const:
    # * 路径
    DATA_ROOT_PATH: str = os.path.join("Dataset")
    Log_ROOT_PATH: str = os.path.join("Log")

    ID2TEXT_NAME: str = "id2text.csv"
    TD2TEXT_COLUMN = ["id", "text"]
    BEHAVIORS_NAME: str = "behaviors.csv"
    BEHAVIORS_COLUMN = ['userid','time','pos_target','full_candidate','full_history']
    # * argparser设定
    MODEL_LIST: List[str] = ["text-davinci-003", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613"]
    MODEL_DEFAULT: str = "gpt-3.5-turbo-0613"
    DOMAIN_LIST: List[str] = ["mind", "job"]
    DOMAIN_DEFAULT: str = "mind"
    TASK_LIST: List[str] = ["Fair-user","Fair-gender","Fair-race", "Fair-nation" , "Fair-continent"]
    TASK_DEFAULT: str = "Fair-gender"
    # * data信息

    # * model设定
    COMPLETION_MODEL_LIST = ["text-davinci-003"]
    CHAT_MODEL_LIST = ["gpt-3.5-turbo-0301","gpt-3.5-turbo-0613"]
    URL_DICT: Dict[str, str] = {
        "gpt-3.5-turbo-0613": "https://api.openai.com/v1/chat/completions",
        "gpt-3.5-turbo-0301": "https://api.openai.com/v1/chat/completions",
        "text-davinci-003": "https://api.openai.com/v1/completions",
        "text-davinci-002": "https://api.openai.com/v1/completions",
        "text-davinci-001": "https://api.openai.com/v1/completions",
    }
    TOKENIZER_DICT: Dict[str, str] = {
        "gpt-3.5-turbo-0613": "cl100k_base",
        "gpt-3.5-turbo-0301": "cl100k_base",
        "text-davinci-003": "p50k_base",
        "text-davinci-002": "p50k_base",
        "text-davinci-001": "r50k_base",
    }