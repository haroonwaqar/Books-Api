from flask import Flask, jsonify, request, render_template
from model import db, Book
from utils.schemas import BookSchema, BookUpdateSchema
import os

app = Flask(__name__)
password = os.environ.get('POSTGRES_PASS')
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{password}@localhost:5432/RestApiData'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

book_schema = BookSchema()
books_schema = BookSchema(many=True)
book_update_schema = BookUpdateSchema()


#GET Request Functions
@app.route('/')
@app.route('/books')
def get_books():
    books = Book.query.all()
    if books:
        return render_template('home.html', books=books)
    else:
        return {"message": "Not found"}, 404
    

@app.route('/books/<int:id>')
def get_a_book(id):
    book = Book.query.filter_by(id=id).first()
    if book:
        return book_schema.dump(book)
    else:
        return ('Book not found', 404)


#POST Request Functions
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400 
    
    book = Book(title=data["title"], author=data["author"])
    db.session.add(book)
    db.session.commit()
    return ('Book is added'), 201
    

#PUT Request Functions
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()

    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    book = Book.query.filter_by(id=id).first()
    if book:
        book.title = data["title"]
        book.author = data["author"]
        db.session.commit()
        return book_schema.dump(book), 200
    else:
        return ('Book not found', 404)
    

#PATCH Request Functions
@app.route('/books/<int:id>', methods=['PATCH'])
def patch_book(id):
    data = request.get_json()

    errors = book_update_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    book = Book.query.filter_by(id=id).first()
    if book:
        if "title" in data:
            book.title = data["title"]
        if "author" in data:
            book.author = data["author"]
        db.session.commit()
        return book_schema.dump(book), 200
    else:
        return ('Book not found', 404)
    

#DELETE Request Functions
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    book = Book.query.filter_by(id=id).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return ('The book has been deleted', 200)
    else:
        return ('Book not found', 404)


#Running
if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)

