import json
from data.preprocessor import PreProcessor
from tqdm import tqdm

def classification_filter(input_path: str, out_racist: str, out_non_racist: str, is_racist_fn):
    
    processor = PreProcessor()

    count = 0
    racist = 0
    nonRacist = 0
    errored_return = 0

    with open(input_path, 'r', encoding='utf-8') as infile, \
         open(out_racist, 'w', encoding='utf-8') as racist_out, \
         open(out_non_racist, 'w', encoding='utf-8') as non_racist_out:
        for line in tqdm(infile, desc="Filtering posts"):

            data = json.loads(line)
            # Filter non-English posts
            if data.get('language') != 'en':
                continue

            cleaned = processor.preprocess(data['content'])

            try:
                content = cleaned['clean_text']
            except Exception as e:
                continue
            count+=1

            racism = is_racist_fn(content)

            if racism is None:
                errored_return+=1
            elif racism:
                racist_out.write(json.dumps(data) + '\n')
                racist+=1
            else:
                non_racist_out.write(json.dumps(data) + '\n')
                nonRacist+=1
            
            if count % 50 == 0:
                print(f"Total treated: {count}\nTotal racists: {racist}\nTotal non-racists: {nonRacist}")
