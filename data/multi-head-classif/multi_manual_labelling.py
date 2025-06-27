import json
import os
from data.preprocessor import PreProcessor

INPUT_FILE = "data/multi-head-classif/racist_posts.jsonl"
TEMP_FILE  = INPUT_FILE + ".tmp"

CATEGORIES = {
    "1": "Racial",
    "2": "Ethnic",
    "3": "Religious",
    "4": "Nationalistic",
    "5": "Political",
    "n": "Not-Racist",
}

def label_data():
    pp = PreProcessor()
    if not os.path.exists(INPUT_FILE):
        print(f"[!] {INPUT_FILE} not found.")
        return

    # Load all lines so we can backtrack and rewrite in place
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    processed = []  # will hold updated JSON-lines or original lines
    index = 0

    # Pre-build the menu string
    menu_lines = ["\nOptions:"]
    for key, name in CATEGORIES.items():
        menu_lines.append(f"  [{key}] = {name}")
    menu_lines += [
        "  [Enter] = skip (leave unlabeled)",
        "  [b]     = backtrack one",
        "  [q]     = quit (save progress)\n"
    ]
    menu = "\n".join(menu_lines)

    while index < len(lines):
        raw = lines[index]
        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            # Invalid JSON: just carry it forward
            processed.append(raw)
            index += 1
            continue

        # Skip anything already labeled
        if data.get("category") in CATEGORIES.values():
            processed.append(raw)
            index += 1
            continue

        # Preprocess and skip if there's no text
        text = pp.preprocess(data.get('content', ""))['clean_text']
        if not text:
            processed.append(raw)
            index += 1
            continue

        # Show the current text and the menu right before asking
        print("\n" + "-" * 60)
        print(f"[{index+1}/{len(lines)}] {text}")
        print(menu)
        choice = input("Choose category: ").strip().lower()

        if choice == "q":
            print("[↩] Quitting and saving progress...")
            break

        if choice == "b":
            if index == 0:
                print("[!] Already at the first item.")
                continue
            # Remove last processed line and step back
            processed.pop()
            index -= 1
            continue

        if choice in CATEGORIES:
            # Assign the chosen category
            data["category"] = CATEGORIES[choice]
            processed.append(json.dumps(data, ensure_ascii=False) + "\n")
        else:
            # Skip labeling: keep original line
            processed.append(raw)

        index += 1

    # Write out what we've processed + the remainder untouched
    with open(TEMP_FILE, 'w', encoding='utf-8') as out:
        out.writelines(processed)
        out.writelines(lines[index:])
    os.replace(TEMP_FILE, INPUT_FILE)

    print(f"\n✅ Done. Progress saved to {INPUT_FILE}")

if __name__ == "__main__":
    label_data()
