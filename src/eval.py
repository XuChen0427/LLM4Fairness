import json
import os
import pandas as pd
import numpy as np
import os
from const import Const as C
import argparse
import random

def Eval(args,type='davinci'):
    if args.task == "Fair-gender":
        names = ["male", "female"]
    elif args.task == "Fair-race":
        names = ["white", "black", "asian"]

    elif args.task == "Fair-continent":
        names = ["Africa", "American", 'oceania', 'Europe']

    elif args.task == "Fair-nation":
        names = ["UK", "US", "AUS"]

    elif args.task == "Fair-user":
        names = ["user"]
    else:
        raise NotImplementedError("Only support task in ", C.TASK_LIST)
    eval_result = {}
    paths = []

    if args.test:
        #input = "request_test"
        input_prefix = "result_test"
    else:
        input_prefix = "result"

    for n in names:
        paths.append(os.path.join(input_prefix, "{}_Result_{}".format(args.domain,str(args.name_id)),args.model,n + "_trial_"+ str(args.trial) +".output"))

    for index,file in enumerate(paths):
        ndcg_list = []
        mrr_list = []
        eval_result[names[index]] = []
        with open(file,'r') as f:
            result = f.readlines()
            for line in result:

                content = json.loads(line)
                for dicts in content:
                    if "pos_target" in dicts.keys():
                        pos_target = int(dicts["pos_target"])
                    if type == 'davinci':
                        if "choices" in dicts.keys():
                            text = dicts["choices"][0]["text"].replace(" ",'')
                    else:
                        if "choices" in dicts.keys():
                            text = dicts["choices"][0]["message"]["content"].replace(" ",'')

                ranking_list = text.split(',')
                topk_list = ranking_list[:args.topk]
                pos_chr = chr(ord('A') + pos_target)
                if pos_chr not in topk_list:
                    ndcg = 0
                    mrr = 0
                else:
                    ndcg = 1/np.log2(topk_list.index(pos_chr)+2)
                    mrr = 1/(topk_list.index(pos_chr)+1)

                ndcg_list.append(ndcg)
                mrr_list.append(mrr)

            if args.metric == 'ndcg':
                eval_result[names[index]].append(np.mean(ndcg_list))
            else:
                eval_result[names[index]].append(np.mean(mrr_list))

    print(eval_result)
    return eval_result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, choices=C.MODEL_LIST, default=C.MODEL_DEFAULT)
    parser.add_argument("--domain", type=str, choices=C.DOMAIN_LIST, default=C.DOMAIN_DEFAULT)
    parser.add_argument("--task", type=str, choices=C.TASK_LIST, default=C.TASK_DEFAULT)
    parser.add_argument("--topk", type=int, choices=[1,3,5], default=5)
    parser.add_argument("--name_id", type=int, choices=[1, 2, 3], default=1)
    parser.add_argument("--trial", type=int, choices=[1, 2, 3], default=1)
    parser.add_argument("--metric", type=str, choices=['ndcg', 'mrr'], default='ndcg')
    parser.add_argument("--test", type=bool, default=True)

    args, unknown = parser.parse_known_args()
    Eval(args, type='chatgpt')



