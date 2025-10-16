# from flask_restful import Resource
# from flask import request
# import json
#
# books = [{"id": 1, "title": "Java book"},
#          {"id": 2, "title": "Python book"}]
#
#
# class BooksGETResource(Resource):
#     def get(self):
#         return books
#
# class BookGETResource(Resource):
#     def get(self, id):
#         for book in books:
#             if book["id"] == id:
#                 return book
#         return None
#
#
# class BookPOSTResource(Resource):
#     def post(self):
#         book = json.loads(request.data)
#         new_id = max(book["id"] for book in books) + 1
#         book["id"] = new_id
#         books.append(book)
#         return book
#
#
# class BookPUTResource(Resource):
#     def put(self, id):
#         book = json.loads(request.data)
#         for _book in books:
#             if _book["id"] == id:
#                 _book.update(book)
#                 return _book
#
#
# class BookDELETEResource(Resource):
#     def delete(self, id):
#         global books
#         books = [book for book in books if book["id"] != id]
#         return "", 204

from flask_restful import Resource
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy

# Assuming this db will be initialized in application.py
db = SQLAlchemy()

# ---------------------
# Book Model Definition
# ---------------------
class Book(db.Model):
    __tablename__ = 'books'  # Optional: explicitly name the table
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# ----------------------------
# Resource: Get All Books
# ----------------------------
class BooksGETResource(Resource):
    def get(self):
        books = Book.query.all()
        return [book.to_dict() for book in books], 200

# ----------------------------
# Resource: Get Single Book
# ----------------------------
class BookGETResource(Resource):
    def get(self, id):
        book = Book.query.get(id)
        if book:
            return book.to_dict(), 200
        return {"message": "Book not found"}, 404

# ----------------------------
# Resource: Create New Book
# ----------------------------
class BookPOSTResource(Resource):
    def post(self):
        data = request.get_json()
        title = data.get("title")

        if not title:
            return {"message": "Title is required"}, 400

        book = Book(title=title)
        db.session.add(book)
        db.session.commit()
        return book.to_dict(), 201

# ----------------------------
# Resource: Update a Book
# ----------------------------
class BookPUTResource(Resource):
    def put(self, id):
        book = Book.query.get(id)
        if not book:
            return {"message": "Book not found"}, 404

        data = request.get_json()
        title = data.get("title")
        if title:
            book.title = title
            db.session.commit()
        return book.to_dict(), 200

# ----------------------------
# Resource: Delete a Book
# ----------------------------
class BookDELETEResource(Resource):
    def delete(self, id):
        book = Book.query.get(id)
        if not book:
            return {"message": "Book not found"}, 404

        db.session.delete(book)
        db.session.commit()
        return {"message": "Deleted"}, 204
