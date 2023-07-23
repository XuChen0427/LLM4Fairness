import os
import json
import pandas as pd
import copy
from typing import List

from const import Const as C


def generate_chatgpt_request(candidate, history, id2text:dict, model: str, candidate_num: int, Prompt, pos_target):

    num = len(Prompt.name)
    request_list = [[] for i in range(num)]
    for i in range(len(candidate)):
        task_id = i
        fmt_dict = {"history": '. '.join([id2text[h] for h in history[i]]),
                    "candidate": '. '.join(["("+chr(ord('A') + j)+") " + id2text[h] for j,h in enumerate(candidate[i])])}
        max_token = 2048
        prompt_list = Prompt.generate_prompt(
            fmt_dict=fmt_dict
        )

        for j,prompt in enumerate(prompt_list):
            #print(prompt)
            #print("================")
            if model in C.COMPLETION_MODEL_LIST:
                request = {
                    "model": model,
                    "prompt": prompt,
                    "max_tokens": max_token,
                    "temperature": 0.2,
                    "top_p": 1,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0,
                    #"logit_bias": log_bias,
                }

                request_list[j].append({
                    "task_id": task_id,
                    "pos_target": int(pos_target[i]),
                    #"target_index": target_index,
                    "request": request,
                    }
                )
            elif model in C.CHAT_MODEL_LIST:
                request = {
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    #"pos_target": int(pos_target[i]),
                    "max_tokens": max_token,
                    "temperature": 0.2,
                    "top_p": 1,
                    "frequency_penalty": 0.0,
                    "presence_penalty": 0.0,
                    #"logit_bias": log_bias,
                }
                request_list[j].append({
                    "task_id": task_id,
                    "pos_target": int(pos_target[i]),
                    # "target_index": target_index,
                    "request": request,
                }
                )
            else:
                raise ValueError("Not supported model type, please check!")

    return request_list

def save_request_file(request_path: str, request_list: list):
    with open(request_path, "w") as f:
        for request in request_list:
            json_string = json.dumps(request)
            f.write(f"{json_string}\n")