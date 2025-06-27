Uses the trained setfit model to refilter the scraped outputs

Once thats done simply execute with:

```
python -m data.second_stage_classification.setfit_binary --model data/racist_binary_classif/best-setfit-model --input data/second_stage_classification/output_timeline.jsonl --out-racist data/second_stage_classification/racist_posts.jsonl --out-non-racist data/second_stage_classification/clean_posts.jsonl
```

to filter by id execute
```
python -m data.second_stage_classification.filter_by_id data/second_stage_classification/clean_posts.jsonl data/second_stage_classification/racist_posts.jsonl
'''