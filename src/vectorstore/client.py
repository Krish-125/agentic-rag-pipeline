# handles the actual connection, and the insert/search functions
import os
import dotenv
from pgvector.psycopg2 import register_vector
import psycopg2
from psycopg2.extras import Json

def get_connection():
    # return a connection to the vector store
    dotenv.load_dotenv()
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    register_vector(conn)
    return conn

def insert_chunks(conn, documents, embedding_model):
    # insert the document chunks into the database
    cur = conn.cursor()
    for doc in documents:
        content = doc.page_content
        metadata = doc.metadata
        embedding = embedding_model.embed_query(content)
        
        cur.execute(
            "INSERT INTO document_chunks (content, metadata, embedding) VALUES (%s, %s, %s)",
            (content, Json(metadata), embedding)
        )
    conn.commit()
    cur.close()