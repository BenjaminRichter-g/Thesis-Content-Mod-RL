import argparse
from setfit import SetFitModel
import json

from data.classification_filter import classification_filter

def is_racist(text: str) -> bool:
    """
    Uses SetFit model to classify the text.
    Assumes binary classification: 1 = racist, 0 = non-racist.
    """
    try:
        return bool(model.predict([text])[0])
    except Exception:
        return None
    

def remove_test_data(input_file):
    """
    Used to remove any data which might have been used for training from the dataset which is being filtered
    """
    ids = set()
    with open('data/racist_binary_classif/labeled.jsonl', encoding='utf-8') as label_file:
        for line in label_file:
            ids.add(json.loads(line)['id'])

    filtered = []
    with open(input_file, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            record = json.loads(line)
            if record['id'] not in ids:
                filtered.append(record)

    with open(input_file, 'w', encoding='utf-8') as f:
        for record in filtered:
            f.write(json.dumps(record) + '\n')

    print(f'Done cleaing, removed {len(filtered)} which existed in the training dataset')

    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Filter JSONL posts using a SetFit binary classifier for racism."
    )
    parser.add_argument('--model', required=True, help="Path to your trained SetFit model directory")
    parser.add_argument('--input', required=True, help="Input JSONL file")
    parser.add_argument('--out-racist', required=True, help="Output JSONL for racist posts")
    parser.add_argument('--out-non-racist', required=True, help="Output JSONL for non-racist posts")
    args = parser.parse_args()
    
    model = SetFitModel.from_pretrained(args.model)

    remove_test_data(args.input)

    classification_filter(args.input, args.out_racist, args.out_non_racist, is_racist)


