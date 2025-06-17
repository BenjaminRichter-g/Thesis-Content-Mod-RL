




with open(path, 'r') as file:
    for line in file:
        data = line.strip()
        data = json.loads(data)
        if data['language'] != 'en':
            continue

        cleaned_content = self.processesor.preprocess(data['content'])
        content = cleaned_content['clean_text']
        hashtags = cleaned_content['hashtags']
        emojis = cleaned_content['emoji_names']
        self.db.add_data(content, hashtags, emojis, data['account']['username'], data["created_at"], data["bot"], data["sensitive"], data)

