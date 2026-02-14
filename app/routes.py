from app import app, db
from app.models import Book, Author, Loan
from app.forms import BookForm, LoanForm
from flask import render_template, redirect, url_for, request

# Lista książek + dodawanie nowej
@app.route("/books/", methods=["GET", "POST"])
def books_list():
    form = BookForm()
    if form.validate_on_submit():
        book = Book(
            title=form.title.data,
            description=form.description.data,
            on_shelf=form.on_shelf.data
        )
        for name in [n.strip() for n in form.authors.data.split(",")]:
            author = Author.query.filter_by(name=name).first()
            if not author:
                author = Author(name=name)
                db.session.add(author)
            book.authors.append(author)
        db.session.add(book)
        db.session.commit()
        return redirect(url_for("books_list"))

    books = Book.query.all()
    return render_template("books.html", books=books, form=form)

# Szczegóły książki + wypożyczenia
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

    # Aktualizacja książki
    if form.validate_on_submit() and 'title' in request.form:
        book.title = form.title.data
        book.description = form.description.data
        book.on_shelf = form.on_shelf.data

        # Aktualizacja autorów
        # usuń wszystkie powiązania z autorami
        book.authors = []

        # dodaj nowe powiązania
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

    # Dodawanie wypożyczenia
    if loan_form.validate_on_submit() and 'borrower' in request.form:
        if book.on_shelf:
            loan = Loan(book=book, borrower=loan_form.borrower.data)
            book.on_shelf = False
            db.session.add(loan)
            db.session.commit()
        return redirect(url_for("book_details", book_id=book.id))

    return render_template("book.html", book=book, form=form, loan_form=loan_form)

# Usuń książkę
@app.route("/books/<int:book_id>/delete/", methods=["POST"])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return redirect(url_for("books_list"))

# Oznacz zwrot książki
@app.route("/loans/<int:loan_id>/return/", methods=["POST"])
def return_loan(loan_id):
    loan = Loan.query.get_or_404(loan_id)
    loan.return_date = db.func.now()
    loan.book.on_shelf = True
    db.session.commit()
    return redirect(url_for("book_details", book_id=loan.book.id))
