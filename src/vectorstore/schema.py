# defines the table and creates it if it doesn't exist
def create_table(conn):
    cur = conn.cursor()
    cur.execute('CREATE EXTENSION IF NOT EXISTS vector')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS document_chunks (
            id SERIAL PRIMARY KEY,
            content TEXT NOT NULL,
            metadata JSONB,
            embedding vector(384)
        )
    ''')

    conn.commit()