from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId
from utils.schemas import BookSchema, BookUpdateSchema

app = Flask(__name__)

# For mongo db setup locally
client = MongoClient("mongodb://localhost:27017/")
db = client['bookstore']
books_collection = db['books']


book_schema = BookSchema()
books_schema = BookSchema(many=True)
book_update_schema = BookUpdateSchema()


#GET Request Functions
@app.route('/')
@app.route('/books')
def get_books():

    books = list(books_collection.find())

    if books:     
        return jsonify(books_schema.dump(books)), 200
        #return rendertemplate('home.html, books=books)
    else:
        return {"message": "Not found"}, 404
    

@app.route('/books/<id>')
def get_a_book(id):
    
    try:
        book = books_collection.find_one({'_id': ObjectId(id)})

        if book: 
            return jsonify(book_schema.dump(book))
        else:
            return ('Book not found', 404)
        
    except InvalidId:
        return {'error': 'Invalid book ID'}, 400


#POST Request Functions
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400 
    
    results = books_collection.insert_one({
        'title': data['title'],
        'author': data['author']
    })
    
    return jsonify({'id': str(results.inserted_id)}), 201
    

#PUT Request Functions
@app.route('/books/<string:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()

    errors = book_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    book = books_collection.find_one({'_id': ObjectId(id)})
    if book:
        books_collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': {"title": data["title"], "author": data["author"]}}
        )
        updated_book = books_collection.find_one({'_id': ObjectId(id)})
        return jsonify(book_schema.dump(updated_book))
    else:
        return ('Book not found', 404)
    

#PATCH Request Functions
@app.route('/books/<id>', methods=['PATCH'])
def patch_book(id):
    data = request.get_json()

    errors = book_update_schema.validate(data)
    if errors:
        return jsonify(errors), 400
    
    book = books_collection.find_one({'_id': ObjectId(id)})
    if book:
        update_data = {}
        if 'title' in data:
            update_data['title'] = data['title']
        if 'author' in data:
            update_data['author'] = data['author']

        books_collection.update_one({'_id': ObjectId(id)}, {'$set': update_data})

        updated_book = books_collection.find_one({'_id': ObjectId(id)})
        return jsonify(book_schema.dump(updated_book)), 200
    
    else:
        return ('Book not found', 404)
    

#DELETE Request Functions
@app.route('/books/<string:id>', methods=['DELETE'])
def delete_book(id):

    book = books_collection.find_one({'_id': ObjectId(id)} )
    if book:
        books_collection.delete_one({'_id': ObjectId(id)})
        return ('The book has been deleted', 200)

    else: 
        return ('Book not found', 404)


#Running
if __name__ == '__main__':
    app.run(debug=True)

