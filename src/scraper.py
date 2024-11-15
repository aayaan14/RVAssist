import sqlite3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import fitz  

def create_db():
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS web_pages (
            url TEXT PRIMARY KEY,
            content TEXT,
            content_type TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def insert_data(url, content, content_type):
    conn = sqlite3.connect('scraped_data.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO web_pages (url, content, content_type)
        VALUES (?, ?, ?)
    ''', (url, content, content_type))
    conn.commit()
    conn.close()

def scrape_rvce_website(base_url):
    try:
        response = requests.get(base_url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        links = soup.find_all('a', href=True)

        for link in links:
            full_url = urljoin(base_url, link['href'])

            # Only proceed if the URL starts with http/https
            if not full_url.startswith(('http://', 'https://')):
                continue

            # Check if the link is a PDF
            if full_url.endswith('.pdf'):
                try:
                    pdf_text = extract_text_from_pdf(full_url)
                    insert_data(full_url, pdf_text, 'pdf')
                except Exception as e:
                    print(f"Error extracting PDF from {full_url}: {e}")
                continue 

            # Scrape HTML content
            try:
                sub_response = requests.get(full_url)
                sub_response.raise_for_status()
                sub_soup = BeautifulSoup(sub_response.text, 'html.parser')

                page_text = ' '.join(sub_soup.stripped_strings)
                insert_data(full_url, page_text, 'html')
            
            except Exception as e:
                print(f"Error scraping {full_url}: {e}")
    
    except Exception as e:
        print(f"Error accessing {base_url}: {e}")
        return {}

def extract_text_from_pdf(pdf_url):
    response = requests.get(pdf_url)
    response.raise_for_status()

    # Save PDF to a temporary file and read with PyMuPDF
    with open("temp.pdf", "wb") as temp_pdf:
        temp_pdf.write(response.content)

    # Extract text from each page
    text = ""
    with fitz.open("temp.pdf") as pdf_document:
        for page_num in range(pdf_document.page_count):
            page = pdf_document.load_page(page_num)
            text += page.get_text()

    return text

if __name__ == "__main__":
    create_db()
    base_url = "https://rvce.edu.in"  
    scrape_rvce_website(base_url)
