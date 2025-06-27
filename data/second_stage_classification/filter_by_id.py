import json
import sys

# Simple in-place filter: two JSONL files (ids + data), rewrite second file with matching records
if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} ids.jsonl input.jsonl", file=sys.stderr)
    sys.exit(1)

ids_file, input_file = sys.argv[1], sys.argv[2]

# Load all IDs from the first file
ids = set()
with open(ids_file, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        ids.add(json.loads(line)['id'])

# Read and filter the second file
filtered = []
with open(input_file, encoding='utf-8') as f:
    for line in f:
        line = line.strip()
        if not line:
            continue
        record = json.loads(line)
        if record['id'] in ids:
            record['label']=1
            filtered.append(record)

# Overwrite the second file with filtered records
with open(input_file, 'w', encoding='utf-8') as f:
    for record in filtered:
        f.write(json.dumps(record) + '\n')
