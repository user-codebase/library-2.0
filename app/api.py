from flask import jsonify, request, abort
from app import app, db
from app.models import Book, Author

@app.route("/api/v1/books/", methods=["GET", "POST"])
def api_books():
    if request.method == "GET":
        books = Book.query.all()
        return jsonify([
            {"id": b.id, "title": b.title, "authors": [a.name for a in b.authors],
             "description": b.description, "on_shelf": b.on_shelf} for b in books
        ])

    data = request.get_json()
    if not data or not all(k in data for k in ("title", "authors", "description")):
        abort(400)

    book = Book(title=data["title"], description=data["description"], on_shelf=data.get("on_shelf", True))
    for name in data["authors"].split(","):
        name = name.strip()
        author = Author.query.filter_by(name=name).first()
        if not author:
            author = Author(name=name)
        book.authors.append(author)

    db.session.add(book)
    db.session.commit()

    return jsonify({"id": book.id, "title": book.title,
                    "authors": [a.name for a in book.authors],
                    "description": book.description,
                    "on_shelf": book.on_shelf}), 201


@app.route("/api/v1/books/<int:book_id>/", methods=["GET", "PUT", "DELETE"])
def api_book_detail(book_id):
    book = Book.query.get_or_404(book_id)

    if request.method == "GET":
        return jsonify({"id": book.id, "title": book.title,
                        "authors": [a.name for a in book.authors],
                        "description": book.description,
                        "on_shelf": book.on_shelf})

    if request.method == "PUT":
        data = request.get_json()
        if not data:
            abort(400)

        book.title = data.get("title", book.title)
        book.description = data.get("description", book.description)
        book.on_shelf = data.get("on_shelf", book.on_shelf)

        if "authors" in data:
            book.authors.clear()
            for name in data["authors"].split(","):
                name = name.strip()
                author = Author.query.filter_by(name=name).first()
                if not author:
                    author = Author(name=name)
                book.authors.append(author)

        db.session.commit()
        return jsonify({"id": book.id, "title": book.title,
                        "authors": [a.name for a in book.authors],
                        "description": book.description,
                        "on_shelf": book.on_shelf})

    if request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return jsonify({"result": True})
