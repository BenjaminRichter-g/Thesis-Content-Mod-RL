import json
import os
from data.preprocessor import PreProcessor

INPUT_FILE = "data/racist_binary_classif/unlabeled.jsonl"
OUTPUT_FILE = "data/racist_binary_classif/labeled.jsonl"
TEMP_FILE = "data/racist_binary_classif/unlabeled_tmp.jsonl"
BACKUP_FILE = "data/racist_binary_classif/labeled_backup.jsonl"

def label_data():
    pp = PreProcessor()
    if not os.path.exists(INPUT_FILE):
        print(f"[!] {INPUT_FILE} not found.")
        return

    # Read all lines into memory to enable going back
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    labeled = []
    skipped = []
    index = 0

    print("\nInstructions:")
    print("  [y] = racist")
    print("  [n] = non-racist")
    print("  [Enter] = skip")
    print("  [b] = go back one")
    print("  [q] = quit\n")

    while index < len(lines):
        line = lines[index]
        try:
            data = json.loads(line)
            text = pp.preprocess(data['content'])
            text = text['clean_text']
            if not text:
                index += 1
                continue

            print("\n" + "-" * 60)
            print(f"[{index+1}/{len(lines)}] {text}")
            label = input("Label [y/n/Enter to skip, b to backtrack, q to quit]: ").strip().lower()

            if label == "q":
                print("\n[↩] Exiting...")
                break
            elif label == "b":
                if labeled:
                    print("[⏪] Backtracking one item.")
                    index -= 1
                    labeled.pop()
                else:
                    print("[!] Nothing to undo.")
            elif label == "y":
                data["label"] = 1
                labeled.append(data)
                index += 1
            elif label == "n":
                data["label"] = 0
                labeled.append(data)
                index += 1
            else:
                skipped.append(line)
                index += 1

        except json.JSONDecodeError:
            index += 1
            continue

    # Write labeled data
    if labeled:
        # Back up previous labeled file if it exists
        if os.path.exists(OUTPUT_FILE):
            os.replace(OUTPUT_FILE, BACKUP_FILE)
            print(f"[💾] Previous labeled file backed up to {BACKUP_FILE}")

        with open(OUTPUT_FILE, 'w', encoding='utf-8') as out:
            for item in labeled:
                out.write(json.dumps(item) + '\n')

    # Save remaining/skipped items back to the input file
    with open(INPUT_FILE, 'w', encoding='utf-8') as out:
        for i in range(index, len(lines)):
            out.write(lines[i])
        for s in skipped:
            out.write(s)

    print("\n✅ Done. Progress saved to:")
    print(f"   Labeled     → {OUTPUT_FILE}")
    print(f"   Remaining   → {INPUT_FILE}")

if __name__ == "__main__":
    label_data()
