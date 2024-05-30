from openai import OpenAI
import os
import pandas as pd
import numpy as np
import tiktoken
import psycopg2
import pgvector
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector

openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

db_host = 'sacm-embedding-db.cv0ky2ics36z.eu-central-1.rds.amazonaws.com'
db_name = 'sacm-db'
db_user = 'postgres'
db_password = '8864baK0xSvipmX5DQls'
db_port = '5432'

embedding_model = "text-embedding-3-small"
encoding_name = "cl100k_base"

def db_connect():
    try:
        connection = psycopg2.connect(
            host=db_host,
            database=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )

        cursor = connection.cursor()
        return connection, cursor

    except Exception as error:
        print(f"Fehler beim Verbinden zur Datenbank: {error}")

def db_query(query:str):
    connection, cursor = db_connect()
    cursor.execute(query)
    result = cursor.fetchall()
    connection.close()
    return result

def push_to_db(filename:str, tablename:str):
    connection, cursor = db_connect()
    df = pd.read_csv(filename)
    data_list = [(row['question'], row['tokens'], np.array(row['question_embedding']).tolist(), row['response_audiofile'], row['response']) for index, row in df.iterrows()]
    #print(data_list)
    query = f"INSERT INTO {tablename} (question, tokens, question_embedding, response_audiofile, response) VALUES %s"
    execute_values(cursor, query, data_list)
    connection.commit()
    connection.close()

def get_embedding_for_csv(filename:str) -> list:
    df = pd.read_csv(filename)
    print(df)
    for index, row in df.iterrows():
        #get embedding
        embedding = openai_client.embeddings.create(
            model = embedding_model,
            input = row['question'],
            encoding_format="float"
        )
        df.at[index, 'question_embedding'] = str(embedding.data[0].embedding)
        #get number of tokens
        encoding = tiktoken.get_encoding(encoding_name)
        df.at[index, 'tokens'] = get_num_of_tokens(row['question'])
    
    df.to_csv(filename, index=False)

def get_num_of_tokens(string:str) -> str:
    if not string:
        return 0
    encoding = tiktoken.get_encoding(encoding_name)
    print(len(encoding.encode(string)))
    return len(encoding.encode(string))

get_embedding_for_csv("small_talk.csv")
#push_to_db("small_talk.csv", "embeddings")