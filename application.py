from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# books_list = [
#     {
#         "id": 0,
#         "author": "Chinua Achebe",
#         "language": "English",
#         "title": "Things Fall Apart",
#     },
#     {
#         "id": 1,
#         "author": "Hans Christian Andersen",
#         "language": "Danish",
#         "title": "Fairy tales",
#     },
#     {
#         "id": 2,
#         "author": "Samuel Beckett",
#         " language": "French, English",
#         "title": "Molloy, Malone Dies",
#     },
#     {
#         "id": 3,
#         "author": "Giovanni Boccaccio",
#         " language": "Italian",
#         "title": "The Decameron",
#     },
#     {
#         "id": 4,
#         "author": "Jorge Luis Borges",
#         " language": "Spanish",
#         "title": "Ficciones",
#     },
#     {
#         "id": 5,
#         "author": "Emily Bront",
#         " language": "English",
#         "title": "Wuthering Heights",
#     },
# ]

def db_connection():
    conn = None
    try:
        conn = sqlite3.connect("books.sqlite")
    except sqlite3.error as e:
        print(e)
    return conn

@app.route('/books', methods=['GET', 'POST'])
def books():
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor = conn.execute("SELECT * FROM book")
        books = [
            dict(id=row[0], author=row[1], language=row[2], title=row[3])
            for row in cursor.fetchall()

        ]
        if books is not None:
            return jsonify(books)

    if request.method == 'POST':
        new_author = request.form['author']
        new_language = request.form['language']
        new_title = request.form['title']
        sql = """INSERT INTO book (author, language, title) VALUES (?, ?, ?)"""
        cursor = cursor.execute(sql, (new_author, new_language, new_title))
        conn.commit()

        return f"Book with the id: {cursor.lastrowid} created successfully", 201

@app.route('/book/<int:id>', methods=['GET','PUT', 'DELETE'])
def single_book(id):
    conn = db_connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM book WHERE id=?", (id,))
        rows = cursor.fetchall()
        for r in rows:
            book = r
        if book is not None:
            return jsonify(book), 200
        else:
            return "Something wrong", 404

    if request.method == 'PUT':
        sql = """UPDATE book
                SET title=?,
                    author=?,
                    language?
                WHERE id=? """
        author = request.form['author']
        language = request.form['language']
        title = request.form['title']
        updated_book = {
            'id': id,
            'author': author,
            'language': language,
            'title': title
        }
        conn.execute(sql, (author, language, title, id))
        conn.commit()
        return jsonify(updated_book)

    if request.method == 'DELETE':
        sql = """ DELETE FROM book WHERE id=? """
        conn.execute(sql, (id,))
        conn.commit()
        return "The book with id: {} has been deleted".format(id), 200

if __name__ == '__main__':
    app.run()