import psycopg2
from dotenv import dotenv_values


class Database:

    def __init__(self):
        config = dotenv_values(".env")
        try:    
            self.conn = psycopg2.connect(database=config["DB_NAME"],
                                    user=config["DB_USER"],
                                    password=config["DB_PASS"],
                                    host=config["DB_HOST"],
                                    port=config["DB_PORT"])
            print("Database connected successfully")
            self.create_db()
        except Exception as e:
            print(e)
            print("Database not connected successfully")


    def create_db(self):
        with self.conn:
            cur = self.conn.cursor()  # creating a cursor
            
            #TODO check if user data needs purging
            cur.execute("""
            CREATE TABLE IF NOT EXISTS labelled_data ( 
                        id SERIAL PRIMARY KEY,
                        content TEXT NOT NULL,
                        hashtags TEXT[],
                        emojis TEXT[],
                        user VARCHAR(50),
                        label_source VARCHAR(10) CHECK (label_source IN ('human', 'setfit')),
                        label_certainties REAL,
                        post_date TIMESTAMP NOT NULL,
                        bot BOOLEAN DEFAULT FALSE,
                        sensitive BOOLEAN DEFAULT FALSE,
                        metadata JSONB
                    );        
            """)
            self.conn.commit()


    def add_data(self, content, hashtags, emojis, user, post_date, bot, sensitive, metadata):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO labelled_data (content, hashtags, emojis, user, post_date, bot, sensitive, metadata)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (content, hashtags, emojis, user, post_date, bot, sensitive, metadata))
            self.conn.commit()

    def label_existing_data(self, serial, label_source, label_certainty):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE labelled_data
                SET label_source = %s, label_certainties = %s
                WHERE id = %s;
            """, (label_source, label_certainty, serial))
            self.conn.commit()


    def label_data(self, post_text, label_source, label_certainty, post_date, bot, sensitive, metadata):
        
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO labelled_data (content, user, label_source, label_certainties, post_date, bot, sensitive, metadata)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (post_text, 'unknown', label_source, label_certainty, post_date, bot, sensitive, metadata))
            self.conn.commit()
