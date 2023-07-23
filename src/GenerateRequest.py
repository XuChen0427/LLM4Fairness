import pandas as pd
import os
import json
#import openai
import argparse
from const import Const as C
from prompt import Prompt
from request_format import generate_chatgpt_request, save_request_file
import numpy as np

import json

def main(args):
    str_file = "topk_candidate@{}_history@{}.csv".format(str(args.candidate_num),str(args.history_num))
    file_path = os.path.join("data","{}_data_process\LLM4Fairness\processed".format(args.domain), str_file)
    behaviors = pd.read_csv(file_path, delimiter='\t')
    Prompt_Generator = Prompt(domain=args.domain, task=args.task)


    behaviors = behaviors[["userid", "itemid_history", "pos_target_index", "itemid_candidate"]]
    behaviors["itemid_history"] = behaviors["itemid_history"].apply(lambda x: x[1:-1].split(', '))
    history = behaviors['itemid_history'].values
    behaviors["itemid_candidate"] = behaviors["itemid_candidate"].apply(lambda x: x[1:-1].split(', '))
    candidate = behaviors['itemid_candidate'].values
    pos_target = behaviors['pos_target_index'].values
    id2text_path = os.path.join("data","{}_data_process\LLM4Fairness\processed".format(args.domain), "title_datamaps.json")

    with open(id2text_path,'r') as f:
        id2text_dict = json.load(f)['id2item_dict']
    request_list = generate_chatgpt_request(candidate=candidate, history=history,
                                            id2text=id2text_dict, model = args.model,
                                            candidate_num=args.candidate_num,
                                            Prompt=Prompt_Generator,
                                            pos_target=pos_target)
    names = Prompt_Generator.name
    num_type = len(names)
    if args.test == False:
        max_index = 300
        outdir = "request"
    else:
        max_index = 50
        outdir = "request_test"

    for i in range(num_type):
        name = names[i] + "_candidate@{}_history@{}".format(str(args.candidate_num),str(args.history_num)) + ".request"
        output_path = os.path.join(outdir, '{}_Request_{}'.format(args.domain, str(args.name_id)), args.model)
        os.makedirs(output_path, exist_ok=True)

        with open(os.path.join(output_path, name), 'w') as f:

            for index, request in enumerate(request_list[i]):
                if index > max_index:
                    break
                json_string = json.dumps(request)
                f.write(f"{json_string}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, choices=C.MODEL_LIST, default=C.MODEL_DEFAULT)
    parser.add_argument("--domain", type=str, choices=C.DOMAIN_LIST, default=C.DOMAIN_DEFAULT)
    parser.add_argument("--task", type=str, choices=C.TASK_LIST, default=C.TASK_DEFAULT)
    parser.add_argument("--history_num", type=int, default=5)
    parser.add_argument("--candidate_num", type=int, default=5)
    parser.add_argument("--name_id", type=int, choices=[1,2,3], default=1)
    parser.add_argument("--test", type=bool, default=True)
    args, unknown = parser.parse_known_args()

    main(args)