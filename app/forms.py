from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class BookForm(FlaskForm):
    title = StringField("Tytuł", validators=[DataRequired()])
    authors = StringField("Autorzy (oddziel przecinkami)", validators=[DataRequired()])
    description = TextAreaField("Opis", validators=[DataRequired()])
    on_shelf = BooleanField("Na półce?")
    submit = SubmitField("Zapisz")

class LoanForm(FlaskForm):
    borrower = StringField("Imię i nazwisko pożyczającego", validators=[DataRequired()])
    submit = SubmitField("Wypożycz")