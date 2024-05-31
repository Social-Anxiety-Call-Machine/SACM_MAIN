from openai import OpenAI
import os
import pandas as pd
import numpy as np
import tiktoken
import psycopg2
import pgvector
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector
from elevenlabs.client import ElevenLabs

class Embedding_utils:

    def __init__(self, voice_id, model_id):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        self.db_host = 'sacm-embedding-db.cv0ky2ics36z.eu-central-1.rds.amazonaws.com'
        self.db_name = 'sacm-db'
        self.db_user = 'postgres'
        self.db_password = '8864baK0xSvipmX5DQls'
        self.db_port = '5432'

        self.embedding_model = "text-embedding-3-small"
        self.encoding_name = "cl100k_base"

        self.voice_id = voice_id
        self.model_id = model_id

        self.eleven_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

    def db_connect(self):
        try:
            connection = psycopg2.connect(
                host=self.db_host,
                database=self.db_name,
                user=self.db_user,
                password=self.db_password,
                port=self.db_port
            )

            cursor = connection.cursor()
            return connection, cursor

        except Exception as error:
            print(f"Fehler beim Verbinden zur Datenbank: {error}")

    def db_query(self, query:str):
        connection, cursor = self.db_connect()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result

    def push_to_db(self, filename:str, tablename:str):
        connection, cursor = self.db_connect()
        df = pd.read_csv(filename)
        data_list = [(row['question'], row['tokens'], np.array(row['question_embedding']).tolist(), row['response_audiofile'], row['response']) for index, row in df.iterrows()]
        #print(data_list)
        query = f"INSERT INTO {tablename} (question, tokens, question_embedding, response_audiofile, response) VALUES %s"
        execute_values(cursor, query, data_list)
        connection.commit()
        connection.close()

    def get_embedding_for_csv(self, filename:str) -> list:
        df = pd.read_csv(filename)
        print(df)
        for index, row in df.iterrows():
            #get embedding
            embedding = self.openai_client.embeddings.create(
                model = embedding_model,
                input = row['question'],
                encoding_format="float"
            )
            df.at[index, 'question_embedding'] = str(embedding.data[0].embedding)
            #get number of tokens
            encoding = tiktoken.get_encoding(encoding_name)
            df.at[index, 'tokens'] = get_num_of_tokens(row['question'])
        
        df.to_csv(filename, index=False)

    def get_num_of_tokens(self, string:str) -> str:
        if not string:
            return 0
        encoding = tiktoken.get_encoding(encoding_name)
        print(len(encoding.encode(string)))
        return len(encoding.encode(string))

    
    def generate_speech_and_save(self, csv_file_path:str):
        df = pd.read_csv(csv_file_path)
        for index, row in df.iterrows():
            text = row['response']
            
            print("Wird generiert und abgespeichert: ", text)
            audio = self.eleven_client.text_to_speech.convert(
                text = text,
                voice_id = self.voice_id,
                model_id = self.model_id
            )

            text = text.replace(" ", "_")
        
            audio_content = b"".join(audio)

            with open(f"../embedding/embedding_audio/{text}.mp3", "wb") as f:
                f.write(audio_content)

    def main(self, csv_file_path:str, table_name:str):
        #self.get_embedding_for_csv(csv_file_path)
        self.generate_speech_and_save(csv_file_path)
        #push_to_db(csv_file_path, table_name)

if __name__ == "__main__":
    eleven = Embedding_utils(voice_id= "VC9NHIQryLjTvEtbF4kj", model_id="eleven_multilingual_v2")
    eleven.main(csv_file_path="../embedding/small_talk.csv", table_name="embeddings")