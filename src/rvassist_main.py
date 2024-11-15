import sqlite3

def load_content_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch Content
    cursor.execute("SELECT url, content FROM web_pages")
    data = cursor.fetchall()

    # Prepare for LlamaIndex
    docs = [{'url': row[0], 'content': row[1]} for row in data]

    return docs
