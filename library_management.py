import sqlite3
from datetime import datetime, timedelta

# Connect to SQLite database (or create it if it doesn’t exist)
conn = sqlite3.connect('library.db')
cursor = conn.cursor()

# Create Books table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Books (
        id INTEGER PRIMARY KEY,
        title TEXT,
        author TEXT,
        genre TEXT,
        available INTEGER DEFAULT 1
    )
''')

# Create Borrowers table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Borrowers (
        id INTEGER PRIMARY KEY,
        name TEXT,
        contact TEXT,
        book_id INTEGER,
        due_date TEXT,
        FOREIGN KEY (book_id) REFERENCES Books(id)
    )
''')

conn.commit()

# Function to add a book
def add_book(title, author, genre):
    cursor.execute("INSERT INTO Books (title, author, genre) VALUES (?, ?, ?)", (title, author, genre))
    conn.commit()
    print(f"Book '{title}' by {author} added successfully.")

# Function to update book details
def update_book(book_id, title=None, author=None, genre=None):
    query = "UPDATE Books SET "
    params = []
    if title:
        query += "title = ?, "
        params.append(title)
    if author:
        query += "author = ?, "
        params.append(author)
    if genre:
        query += "genre = ?, "
        params.append(genre)
    
    query = query.rstrip(", ") + " WHERE id = ?"
    params.append(book_id)
    
    cursor.execute(query, tuple(params))
    conn.commit()
    print(f"Book ID {book_id} updated successfully.")

# Function to delete a book
def delete_book(book_id):
    cursor.execute("DELETE FROM Books WHERE id = ?", (book_id,))
    conn.commit()
    print(f"Book ID {book_id} deleted successfully.")

# Function to borrow a book
def borrow_book(borrower_name, contact, book_id):
    # Check if the book is available
    cursor.execute("SELECT available FROM Books WHERE id = ?", (book_id,))
    result = cursor.fetchone()
    if result and result[0] == 1:
        due_date = (datetime.now() + timedelta(days=14)).strftime('%Y-%m-%d')
        cursor.execute("INSERT INTO Borrowers (name, contact, book_id, due_date) VALUES (?, ?, ?, ?)", 
        (borrower_name, contact, book_id, due_date))
        cursor.execute("UPDATE Books SET available = 0 WHERE id = ?", (book_id,))
        conn.commit()
        print(f"Book ID {book_id} borrowed by {borrower_name}. Due date: {due_date}")
    else:
        print("Book is currently unavailable.")

# Function to return a book
def return_book(book_id):
    cursor.execute("DELETE FROM Borrowers WHERE book_id = ?", (book_id,))
    cursor.execute("UPDATE Books SET available = 1 WHERE id = ?", (book_id,))
    conn.commit()
    print(f"Book ID {book_id} returned successfully.")

# Test the functions
if __name__ == "__main__":
    add_book("Python Programming", "John Doe", "Education")
    update_book(1, author="Jane Doe")
    borrow_book("Alice", "alice@example.com", 1)
    return_book(1)

