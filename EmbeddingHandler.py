from openai import OpenAI
import os
import pandas as pd
import numpy as np
import tiktoken
import psycopg2
import pgvector
from psycopg2.extras import execute_values
from pgvector.psycopg2 import register_vector

class EmbeddingHandler:
    def __init__(self, embedding_threshold):
        self.client = openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.db_host = 'sacm-embedding-db.cv0ky2ics36z.eu-central-1.rds.amazonaws.com'
        self.db_name = 'sacm-db'
        self.db_user = 'postgres'
        self.db_password = '8864baK0xSvipmX5DQls'
        self.db_port = '5432'
        self.embedding_model = "text-embedding-3-small"
        self.embedding_threshold = embedding_threshold

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
            return None, None

    def get_best_match(self, query_embedding, connection, cursor):
        embedding_array = np.array(query_embedding)
        register_vector(connection)
        cursor.execute("SELECT response, (question_embedding <=> %s) AS similarity FROM embeddings ORDER BY similarity LIMIT 1", (embedding_array,))
        best_match = cursor.fetchone()
        
        if best_match:
            response, similarity = best_match
            print(f"Embedding: Best match: {response}, similarity: {similarity}")
            return response, similarity
        else:
            return None, None

    def get_embedding(self, text):
        connection, cursor = self.db_connect()
        if connection is None or cursor is None:
            return False

        embedding = self.client.embeddings.create(
            model = self.embedding_model,
            input = text,
            encoding_format="float"
        )

        best_match, similarity = self.get_best_match(embedding.data[0].embedding, connection, cursor)
        
        if similarity < self.embedding_threshold:
            return best_match
        else:
            return None