Make sure that you have a GPU and are logged in to huggingface + that you requested access to the llama models.

To obtain new data simply run:

```
mastodoner instance --instance-url LINK_TO_INSTANCE --timeline output_timeline.jsonl --limit 1000
```
in our case we used
```
mastodoner instance --instance-url gameliberty.club --timeline output_timeline.jsonl --limit 20000
```


Once thats done simply execute with:

```
python -m data.Scrapping_and_initial_classification.LLM_pre_screening --model meta-llama/Llama-2-7b-chat-hf --input data/Scrapping_and_initial_classification/output_timeline.jsonl --out-racist data/Scrapping_and_initial_classification/racist_posts.jsonl --out-non-racist data/Scrapping_and_initial_classification/clean_posts.jsonl
```
