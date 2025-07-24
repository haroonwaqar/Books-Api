# Flask Books REST API

A simple and clean RESTful API built using **Flask**, **PyMongo**, and **MongoDB**, with full CRUD functionality for managing books. Data is stored in a NoSQL database and can be viewed via MongoDB Compass in a collection named books. It has input validation using Marshmallow. The requests are tested using Postman.

## Features

- `GET /books` — Retrieve all books
- `GET /books/<id>` — Retrieve a single book by ID
- `POST /books` — Add a new book
- `PUT /books/<id>` — Fully update a book
- `PATCH /books/<id>` — Partially update a book
- `DELETE /books/<id>` — Delete a book

## Tech Stack

- **Backend:** Flask
- **ORM:** PyMongo
- **Database:** MongoDB
- **Language:** Python
