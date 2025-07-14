from flask import Flask, jsonify, request
from model import db, Book
import os

app = Flask(__name__)
password = os.environ.get('POSTGRES_PASS')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@localhost:5432/RestApiData'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    book = Book(title=data["title"], author=data["author"])
    db.session.add(book)
    db.session.commit()
    return ('Book is added'), 201


@app.route('/books')
def get_books():
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books])


@app.route('/books/<int:id>')
def get_a_book(id):
    book = Book.query.filter_by(id=id).first()
    if book:
        return jsonify(book.to_dict())
    else:
        return ('Book not found', 404)
    

@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    book = Book.query.filter_by(id=id).first()
    if book:
        book.title = data["title"]
        book.author = data["author"]
        db.session.commit()
        return jsonify(book.to_dict())
    else:
        return ('Book not found', 404)
    

@app.route('/books/<int:id>', methods=['PATCH'])
def patch_book(id):
    data = request.get_json()
    book = Book.query.filter_by(id=id).first()
    if book:
        if "title" in data:
            book.title = data["title"]
        if "author" in data:
            book.author = data["author"]
        db.session.commit()
        return jsonify(book.to_dict())
    else:
        return ('Book not found', 404)
    

@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.filter_by(id=id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return ('The book has been deleted', 200)
    else:
        return ('Book not found', 404)


if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

