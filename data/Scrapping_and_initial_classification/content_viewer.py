from data.preprocessor  import PreProcessor
from tqdm import tqdm
import json

processor = PreProcessor()


with open("data/Scrapping_and_initial_classification/racist_posts.jsonl", 'r', encoding='utf-8') as infile, \
        open("data/Scrapping_and_initial_classification/content_only.jsonl", 'w', encoding='utf-8') as racist_out:
    for line in tqdm(infile, desc="Filtering posts"):
        data = json.loads(line)
        # Filter non-English posts
        if data.get('language') != 'en':
            continue

        cleaned = processor.preprocess(data['content'])

        racist_out.write(json.dumps(cleaned) + '\n')
