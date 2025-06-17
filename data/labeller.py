import db as database
import json
import preprocessor as pp

class LabellerUI:

    def __init__(self):
        self.db = database.Database()
        self.processesor = pp.PreProcessor()


    def consumer(self, path):
        """
        Takes the path to a file containing json data and processes it to be added to the database.
        This simply adds the data to the db without labelling it.
        """
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


    def human_labelling(self):
        """
        This method is used to label the data manually.
        It fetches the data from the database and asks the user to label it.
        """
        data = self.db.get_data_to_label()

        if not data:
            print("No data to label.")
            return

        for item in data:
            print(f"Content: {item['content']}")
            label = input("Enter label (1 for positive, 0 for negative): ")
            self.db.add_label(item['id'], label)
            print(f"Label {label} added for item with id {item['id']}.")
        
            
             


    




