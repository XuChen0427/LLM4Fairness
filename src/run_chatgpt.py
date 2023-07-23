from API.openai import process_api_requests_from_file
import asyncio
import argparse
import os
from const import Const as C
import API.openai
import json
import logging


def GetResultFromGPT(args):
    logging.basicConfig(
        filename="test_gpt.log",
        filemode="w",
        level=logging.INFO,
        format="%(asctime)s %(message)s",
    )
    if args.task == "Fair-gender":
        list = ["male", "female"]
    elif args.task == "Fair-race":
        list = ["white", "black", "asian"]
    elif args.task == "Fair-nation":
        list = ["UK", "US", "AUS"]
    elif args.task == "Fair-continent":
        list = ["Africa", "American", 'oceania', 'Europe']
    elif args.task == "Fair-user":
        list = ["user"]
    else:
        raise NotImplementedError("only support task in",C.TASK_LIST)
    for j in list:

        if args.test:
            input_prefix = "request_test"
            output_predix = "result_test"
        else:
            input_prefix = "request"
            output_predix = "result"


        name = j+ "_candidate@{}_history@{}".format(str(args.candidate_num),str(args.history_num)) + ".request"
        input_file = os.path.join(input_prefix, '{}_Request_{}'.format(args.domain, str(args.name_id)), args.model, name)
        print(input_file)

        outdir = os.path.join(output_predix, '{}_Result_{}'.format(args.domain, str(args.name_id)), args.model)
        os.makedirs(outdir,exist_ok=True)
        outfile = os.path.join(outdir, j + "_trial_"+ str(args.trial) +".output")
        print(outfile)
        asyncio.run(
            process_api_requests_from_file(
                #requests_filepath=os.path.join("request",args.model,j+".request"),
                requests_filepath=input_file,
                save_filepath=outfile,
                request_url=C.URL_DICT[args.model],
                api_key=args.api_key,
                max_requests_per_minute=args.max_requests_per_minute,
                max_tokens_per_minute=args.max_tokens_per_minute,
                token_encoding_name=C.TOKENIZER_DICT[args.model],
                max_attempts=args.max_attempts,
                proxy=args.proxy,
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, choices=C.MODEL_LIST, default=C.MODEL_DEFAULT)
    parser.add_argument("--domain", type=str, choices=C.DOMAIN_LIST, default=C.DOMAIN_DEFAULT)
    parser.add_argument("--task", type=str, choices=C.TASK_LIST, default=C.TASK_DEFAULT)
    parser.add_argument("--history_num", type=int, default=5)
    parser.add_argument("--candidate_num", type=int, default=5)
    parser.add_argument("--request_num", type=int, default=1)
    parser.add_argument("--api_key", type=str, default="your api key")
    parser.add_argument("--max_requests_per_minute", type=int, default=20000)
    parser.add_argument("--max_tokens_per_minute", type=int, default=10000)
    parser.add_argument("--max_attempts", type=int, default=10)
    parser.add_argument("--proxy", type=str, default="your proxy")
    parser.add_argument("--name_id", type=int, choices=[1, 2, 3], default=1)
    parser.add_argument("--trial", type=int, choices=[1,2,3], default=1)
    parser.add_argument("--test", type=bool, default=True)
    args, unknown = parser.parse_known_args()
    GetResultFromGPT(args)