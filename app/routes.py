from app import app, db
from app.models import Book, Author, Loan
from app.forms import BookForm, LoanForm
from flask import render_template, redirect, url_for, request


@app.route("/books/")
def books_list():
    authors = Author.query.order_by(Author.name).all()
    author_id = request.args.get("author_id", type=int)

    if author_id:
        selected_author = Author.query.get_or_404(author_id)
        books = selected_author.books
    else:
        books = Book.query.order_by(Book.title).all()
        selected_author = None

    return render_template("books.html", books=books, authors=authors, selected_author=author_id)


@app.route("/books/add/", methods=["GET", "POST"])
def add_book():
    form = BookForm()

    if form.validate_on_submit():
        book = Book(title=form.title.data, description=form.description.data, on_shelf=form.on_shelf.data)
        db.session.add(book)

        author_names = [n.strip() for n in form.authors.data.split(",") if n.strip()]

        authors = []
        for name in author_names:
            author = Author.query.filter_by(name=name).first()

            if not author:
                author = Author(name=name)
                db.session.add(author)

            authors.append(author)

        book.authors = authors
        db.session.commit()
        return redirect(url_for("books_list"))
    
    return render_template("add_book.html", form=form)

@app.route("/books/<int:book_id>/", methods=["GET", "POST"])
def book_details(book_id):
    book = Book.query.get_or_404(book_id)
    form = BookForm(
        title=book.title,
        authors=", ".join(a.name for a in book.authors),
        description=book.description,
        on_shelf=book.on_shelf
    )
    loan_form = LoanForm()

    if form.validate_on_submit() and 'title' in request.form:
        book.title = form.title.data
        book.description = form.description.data
        book.on_shelf = form.on_shelf.data

        book.authors = []

        for name in form.authors.data.split(","):
            name = name.strip()
            if not name:
                continue
            author = Author.query.filter_by(name=name).first()
            if not author:
                author = Author(name=name)
                db.session.add(author)
            book.authors.append(author)

        db.session.commit()
        return redirect(url_for("books_list"))

    if loan_form.validate_on_submit() and 'borrower' in request.form:
        if book.on_shelf:
            loan = Loan(book=book, borrower=loan_form.borrower.data)
            book.on_shelf = False
            db.session.add(loan)
            db.session.commit()
        return redirect(url_for("book_details", book_id=book.id))

    return render_template("book.html", book=book, form=form, loan_form=loan_form)

@app.route("/books/<int:book_id>/delete/", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("books_list"))

@app.route("/loans/<int:loan_id>/return/", methods=["POST"])
def return_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    loan.return_date = db.func.now()
    loan.book.on_shelf = True
    db.session.commit()
    return redirect(url_for("book_details", book_id=loan.book.id))

@app.route("/authors/<int:author_id>/")
def author_details(author_id):
    author = Author.query.get_or_404(author_id)
    books = author.books
    return render_template("author.html", author=author, books=books)
