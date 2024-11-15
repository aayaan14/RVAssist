import sqlite3

def test_database():
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    c.execute("SELECT * FROM web_pages LIMIT 5")  
    rows = c.fetchall()
    
    if rows:
        print("Data stored in the database:")
        for row in rows:
            url, content, content_type, timestamp = row
            word_count = len(content.split())  # Calculate the number of words in the content
            
            print(f"URL: {url}")
            print(f"Content Type: {content_type}")
            print(f"Timestamp: {timestamp}")
            print(f"Content Preview: {content[:100]}...")  # Preview first 100 chars of content
            print(f"Word Count: {word_count}")
            print("="*80)
    else:
        print("No data found in the database.")
    
    conn.close()

# Test function
if __name__ == "__main__":
    test_database()
