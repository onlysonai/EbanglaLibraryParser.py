# 📚 eBanglaLibrary Book Parser to EPUB
Before running the script, edit the following variables in **parse.py**:

BOOK_NAME = "xyz"

WRITER_NAME = "abc"

BOOK_URL = "https://www.ebanglalibrary.com/books/abcdefxyz"


---

## ⚙️ Requirements

- Python 3.8+
- pip install requests beautifulsoup4 lxml

How to Run
From the project directory:

python3 parse.py

What Happens

1. The script fetches all chapter links from the book page
2. Each chapter is downloaded and parsed
3. XHTML files are saved inside.

✏️ Editing the EPUB with Sigil (Recommended)
1. Open Sigil
2. Create a new EPUB
3. Import all .xhtml files from:
4. book/BOOK_NAME/

Edit:
1. Book title
2. Author name
3. Chapter order
4. Metadata

Add:
1. Cover image
2. Table of Contents

Save the EPUB.
