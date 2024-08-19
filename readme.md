# Underlying Discrimination in New-generation Information Delivery

# environment:
Linux 18.04 python 3.6

# Note: 
We provide the processed dataset at data/.
For news-recommendation (MIND) dataset, please download from https://msnews.github.io/ and store it in Dataset/news/. Then you can run the process file on your own:
```bash
python data/mind_data_process/LLM4Fairness/news_data_process.ipynb
```


For job-recommendation dataset, please download from https://www.kaggle.com/competitions/job-recommendation/data and store it in Dataset/job/. Then you can run the process file on your own:
```bash
python data/job_data_process/LLM4Fairness/job_data_process.ipynb
```

## 1. Generate request for OpenAI API
```bash
python src/GenerateRequest.py [arg1] [arg2] ... [argN]
```
| args_name  | type  | description  |
|---------|---------|---------|
| model | str | Generative model name, we only support in ["text-davinci-003", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613"] |
| domain | str | The tested task domain, we only support in ["mind", "job"] |
| task | str | The tested group, we support ["Fair-user","Fair-gender","Fair-race", "Fair-nation" , "Fair-continent"], where term "Fair-user" denotes there is no given  name to the system. |
| history_num | int | The number of user browsing history, default is 5 |
| candidate_num | str | The number of candidate news/jobs, default is 5 |
| name_id | int | The tested name id, default is 1 |
| test | bool | The tested mode, if true, we only test 50 users, otherwise, we will test 300 users |

## 2. Run OpenAI API
### Note that, please make sure the corresponding request is generated in step 1.
```bash
python src/run_chatgpt.py [arg1] [arg2] ... [argN]
```
| args_name  | type  | description  |
|---------|---------|---------|
| model | str | Generative model name, we only support in ["text-davinci-003", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613"] |
| domain | str | The tested task domain, we only support in ["mind", "job"] |
| task | str | The tested group, we support ["Fair-user","Fair-gender","Fair-race", "Fair-nation" , "Fair-continent"], where term "Fair-user" denotes there is no given  name to the system. |
| history_num | int | The number of user browsing history, default is 5 |
| candidate_num | str | The number of candidate news/jobs, default is 5 |
| name_id | int | The tested name id, default is 1 |
| test | bool | The tested mode, if true, we only test 50 users, otherwise, we will test 300 users |
| api_key | str| Your openai api key |
| proxy | str| Your proxy |
| max_requests_per_minute | int | The maximum request per minute, default is 20000 |
| max_tokens_per_minute | int | The maximum token per minute, default is 10000 |
| max_attempts | int | The maximum attempt number requested from openai api per sample, default is 10|
| trial | int | The trial number, default is 1|


## 3. Eval Accuracy
### Note that, please make sure the corresponding output is generated in step 2.
```bash
python src/eval.py [arg1] [arg2] ... [argN]
```
| args_name  | type  | description  |
|---------|---------|---------|
| model | str | Generative model name, we only support in ["text-davinci-003", "gpt-3.5-turbo-0301", "gpt-3.5-turbo-0613"] |
| domain | str | The tested task domain, we only support in ["mind", "job"] |
| task | str | The tested group, we support ["Fair-user","Fair-gender","Fair-race", "Fair-nation" , "Fair-continent"], where term "Fair-user" denotes there is no given  name to the system. |
| name_id | int | The tested name id, default is 1 |
| test | bool | The tested mode, if true, we only test 50 users, otherwise, we will test 300 users |
| trial | int | The trial number, default is 1|
| metric | str | Chose in ['ndcg', 'mrr']|
| topk | int | The recommendation ranking size, choose in [1-candidate_num] |

## Example Result:
```bash
python src/eval.py
```

Test NDCG@5:
{'male': [0.6357341838863524], 'female': [0.6292297829448893]}




