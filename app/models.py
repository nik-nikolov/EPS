from flask import flash
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import ValidationError

from app import db, login


class User(UserMixin, db.Model):
    # __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True)
    name = db.Column(db.String(64))
    surname = db.Column(db.String(64))
    family = db.Column(db.String(64))
    role = db.Column(db.String(32))
    email = db.Column(db.String(120), index=True)
    password_hash = db.Column(db.String(128))

    def __init__(self, username, name, surname, family, email, role):
        self.username = username
        self.name = name
        self.surname = surname
        self.family = family
        self.email = email
        self.role = role

    def __repr__(self):
        return '<User {}>'.format(self.username, self.name, self.family)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @login.user_loader
    def load_user(self):
        return User.query.get(int(self))


class Citizen(db.Model):
    # __tablename__ = "citizens"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    surname = db.Column(db.String(60))
    family = db.Column(db.String(60))
    egn = db.Column(db.Integer, index=True)
    idcard = db.Column(db.Integer)
    date_of_issue = db.Column(db.Date)
    issued_by = db.Column(db.String(20))
    position = db.Column(db.String(20))
    vote_section = db.Column(db.Integer)
    sum = db.Column(db.Integer)
    email = db.Column(db.String(60))
    tel = db.Column(db.Integer)
    date_of_reg = db.Column(db.DateTime)
    date_of_payment = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Citizen {}>'.format(self.name, self.surname, self.family, self.egn)

    def check_egn(self, egn):
        list_of_ints = [int(x) for x in egn]
        size = len(list_of_ints)
        size_egn = 10
        if size == size_egn:
            data = list_of_ints[0] * 2 + list_of_ints[1] * 4 + list_of_ints[2] * 8 + list_of_ints[3] * 5 + \
                   list_of_ints[
                       4] * 10 + list_of_ints[5] * 9 + list_of_ints[6] * 7 + list_of_ints[7] * 3 + list_of_ints[
                       8] * 6
            data = data % 11
            if data == list_of_ints[9]:
                print("Validen EGN")
            else:
                print("Nevaliden EGN.Molq opitajte otnovo.")
                flash('Невалиден ЕГН.Моля въведете друг ЕГН.')
                raise ValidationError('Невалиден ЕГН.Моля въведете друг ЕГН.')
        else:
            print("ЕГН трябва да е 10-цифрен")
            flash("ЕГН трябва да е 10-цифрен")
            raise ValidationError("ЕГН трябва да е 10-цифрен")


def numbers_to_words(number):  # translate digit to words
    number2word = {'1': "едно", '2': "две", '3': "три", '4': "четири", '5': "пет", '6': "шест",
                   '7': "седем", '8': "осем", '9': "девет", '0': "нула"}
    return " ".join(map(lambda i: number2word[i], str(number)))
