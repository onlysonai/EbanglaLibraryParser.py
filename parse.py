import os
import requests
from bs4 import BeautifulSoup
import time

# -------------------------------
# CONFIG
# -------------------------------
BOOK_NAME = "xyz"
WRITER_NAME = "abc"
BOOK_URL = "https://www.ebanglalibrary.com/books/abcdefxyz"
OUTPUT_DIR = f"book/{BOOK_NAME}"

# -------------------------------
# HELPERS
# -------------------------------
def get_headers():
    return {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

def prettify(html):
    return BeautifulSoup(html, "lxml").prettify()

# -------------------------------
# GET CHAPTER LINKS FROM BOOK PAGE
# -------------------------------
def get_chapter_links(book_url):
    try:
        r = requests.get(book_url, headers=get_headers(), timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        
        links = []
        for a in soup.select("a[href]"):
            href = a.get("href")
            if not href:
                continue
            
            # Filter for chapter links - adjust this based on actual URL patterns
            if href.startswith("https://www.ebanglalibrary.com/") and "/books/" not in href and href != book_url:
                # Exclude common non-chapter pages
                if not any(x in href for x in ['/category/', '/tag/', '/author/', '/about', '/contact', '/search']):
                    links.append(href)
        
        # Remove duplicates, keep order
        seen = set()
        clean_links = []
        for link in links:
            if link not in seen:
                seen.add(link)
                clean_links.append(link)
        
        return clean_links
    except Exception as e:
        print(f"❌ Error fetching book page: {e}")
        return []

# -------------------------------
# PARSE SINGLE CHAPTER
# -------------------------------
def parse_chapter(chapter_url, index):
    try:
        r = requests.get(chapter_url, headers=get_headers(), timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "lxml")
        
        # -------- TITLE --------
        title = ""
        tag = soup.find("span", class_="current-item")
        if tag:
            title = tag.get_text(strip=True)
        
        if not title:
            h1 = soup.find("h1")
            if h1:
                title = h1.get_text(strip=True)
        
        if not title:
            title = f"অধ্যায় {index}"
        
        # -------- CONTENT --------
        body = soup.find("div", class_="entry-content")
        if not body:
            body = soup.find("article")
        
        if not body:
            print(f"⚠️ Content not found, skipping: {chapter_url}")
            return
        
        # -------- WRITE FILE --------
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        filename = f"chapter{str(index).zfill(3)}.xhtml"
        path = os.path.join(OUTPUT_DIR, filename)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0" encoding="utf-8"?>\n')
            f.write('<!DOCTYPE html>\n\n')
            f.write('<html xmlns="http://www.w3.org/1999/xhtml">\n')
            f.write(f"<head>\n  <title>{title}</title>\n</head>\n")
            f.write("<body>\n")
            f.write(f"  <h1>{title}</h1>\n")
            f.write(f"  {body.prettify()}\n")
            f.write("</body>\n")
            f.write("</html>\n")
        
        print(f"✅ Saved: {filename}")
        time.sleep(1)  # Be polite to the server
        
    except Exception as e:
        print(f"❌ Error parsing chapter {index} ({chapter_url}): {e}")

# -------------------------------
# MAIN FUNCTION
# -------------------------------
def parse_full_book():
    chapters = get_chapter_links(BOOK_URL)
    
    if not chapters:
        print("❌ No chapters found.")
        return
    
    print(f"📘 Found {len(chapters)} chapters\n")
    
    for i, url in enumerate(chapters, start=1):
        print(f"{str(i).zfill(2)} {url}")
        parse_chapter(url, i)
    
    print("\n✅ Finished parsing book")

# -------------------------------
# ENTRY POINT
# -------------------------------
if __name__ == "__main__":
    parse_full_book()
