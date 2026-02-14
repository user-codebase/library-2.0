from app import db
from datetime import datetime

authors_books = db.Table(
    'authors_books',
    db.Column('book_id', db.Integer, db.ForeignKey('book.id'), primary_key=True),
    db.Column('author_id', db.Integer, db.ForeignKey('author.id'), primary_key=True)
)


class Author(db.Model):
    __tablename__ = 'author'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False, unique=True)
    books = db.relationship('Book', secondary=authors_books, back_populates='authors')

class Book(db.Model):
    __tablename__ = 'book'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    description = db.Column(db.Text, nullable=False)
    on_shelf = db.Column(db.Boolean, default=True)
    authors = db.relationship('Author', secondary=authors_books, back_populates='books', cascade="all, delete")
    loans = db.relationship('Loan', backref='book', cascade="all, delete-orphan")

class Loan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
    borrower = db.Column(db.String(100), nullable=False)
    loan_date = db.Column(db.DateTime, default=datetime.utcnow)
    return_date = db.Column(db.DateTime, nullable=True)

    @property
    def is_returned(self):
        return self.return_date is not None
