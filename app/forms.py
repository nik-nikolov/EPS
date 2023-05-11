from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, \
    IntegerField, EmailField, FloatField, DateTimeField, DateField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp, Length

from app.models import User, Citizen


class LoginForm(FlaskForm):
    username = StringField('Потребителско име', validators=[DataRequired(message='Задължително поле.')])
    password = PasswordField('Парола', validators=[DataRequired(message='Задължително поле.')])
    remember_me = BooleanField('Запомни ме')
    submit = SubmitField('Изпрати')


class RegistrationForm(FlaskForm):
    username = StringField('Потребителско име', validators=[Length(min=4,
                                                                   message='Потребителско име не по-малко от 4 символа.')])
    name = StringField('Име', validators=[DataRequired(message='Задължително поле.')])
    surname = StringField('Бащино име')
    family = StringField('Фамилия', validators=[DataRequired(message='Задължително поле.')])
    email = EmailField('Email', validators=[Email()])
    role = SelectField('Роля', choices=[], coerce=str, option_widget=None, validate_choice=True,
                       validators=[DataRequired(message='Задължително поле')])
    password = PasswordField('Парола', validators=[DataRequired(message='Задължително поле.'),
                                                   Length(min=6, message='Парола между 6 и 10 символа.'),
                                                   Regexp('^\S*(?=\S{6,})(?=\S*\d)(?=\S*[A-Z])(?=\S*[a-z])'
                                                          '(?=\S*[!@#$%^&*? ])\S*$',
                                                          0,
                                                          message='Паролата трябва да бъде комплексна.')])
    password2 = PasswordField('Повтори Парола',
                              validators=[DataRequired(message='Задължително поле.'), EqualTo('password')])
    submit = SubmitField('Регистрация')

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.role.choices = [('user', 'Потребител'), ('admin', 'Администратор')]

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email is not None:
            raise ValidationError('Моля въведете друг e-mail.')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Моля въведете друго потребителско име.')


class EditingForm(FlaskForm):
    username = StringField('Потребителско име',
                           validators=[Length(min=4, message='Потребителско име не по-малко от 4 символа.')])
    name = StringField('Име')
    surname = StringField('Бащино име')
    family = StringField('Фамилия')
    email = EmailField('Email', validators=[Email()])
    role = SelectField('Роля', choices=[], coerce=str, option_widget=None, validate_choice=True)
    password = PasswordField('Парола', validators=[Length(min=6, max=10, message='Парола между 6 и 10 символа.'),
                                                   Regexp(
                                                       '^\S*(?=\S{6,})(?=\S*\d)(?=\S*[A-Z])(?=\S*[a-z])(?=\S*[!@#$%^&*? ])\S*$',
                                                       0,
                                                       message='Паролата трябва да бъде комплексна.')])
    password2 = PasswordField('Повтори Парола', validators=[EqualTo('password', message='Няма съвпадение на паролите')])
    submit = SubmitField('Редактиране')

    def __init__(self, *args, **kwargs):
        super(EditingForm, self).__init__(*args, **kwargs)
        self.role.choices = [('user', 'Потребител'), ('admin', 'Администратор')]


class CitizenForm(FlaskForm):
    id = IntegerField()
    name = StringField('Име', validators=[DataRequired(message='Задължително поле.')])
    surname = StringField('Презиме')
    family = StringField('Фамилия', validators=[DataRequired(message='Задължително поле.')])
    egn = IntegerField('ЕГН', validators=[DataRequired(message='Задължително поле.')])
    idcard = IntegerField('Номер на Лична Карта', validators=[DataRequired(message='Задължително поле.')])
    date_of_issue = DateField('Дата на издаване ',
                              validators=[DataRequired(message='Задължително поле.')])
    issued_by = StringField('Издадена от:', validators=[DataRequired(message='Задължително поле.')])
    position = SelectField('Длъжност', choices=[], coerce=str, option_widget=None, validate_choice=True)
    vote_section = IntegerField('Изб.секция №', validators=[DataRequired(message='Задължително поле.')])
    sum = FloatField('Възнаграждение', validators=[DataRequired(message='Задължително поле.')])
    email = EmailField('Email')
    # email = EmailField('Email', validators=[Email()])
    tel = IntegerField('Телефон')
    date_of_reg = DateTimeField()
    date_of_payment = DateTimeField()
    submit = SubmitField('Запис')

    def __init__(self, *args, **kwargs):
        super(CitizenForm, self).__init__(*args, **kwargs)
        self.position.choices = [('member', 'член'), ('chairmen', 'председател'),
                                 ('vice chairman', 'зам-председател'), ('secretary', 'секретар'),
                                 ('other', 'друга')]

    def validate_egn(self, egn):
        egn = Citizen.query.filter_by(egn=egn.data).first()
        if egn is not None:
            raise ValidationError('Съществуващ ЕГН.Моля въведете друг ЕГН.')


class EditingCitizenForm(FlaskForm):
    id = IntegerField()
    name = StringField('Име', validators=[DataRequired(message='Задължително поле.')])
    surname = StringField('Презиме')
    family = StringField('Фамилия', validators=[DataRequired(message='Задължително поле.')])
    egn = IntegerField('ЕГН', validators=[DataRequired(message='Задължително поле.')])
    idcard = IntegerField('Номер на Лична Карта', validators=[DataRequired(message='Задължително поле.')])
    date_of_issue = DateField('Дата на издаване: ',
                              validators=[DataRequired(message='Задължително поле.')])
    issued_by = StringField('Издадена от: ', validators=[DataRequired(message='Задължително поле.')])
    position = SelectField('Длъжност', choices=[], coerce=str, option_widget=None, validate_choice=True)
    vote_section = IntegerField('Изб.секция №', validators=[DataRequired(message='Задължително поле.')])
    sum = FloatField('Възнаграждение', validators=[DataRequired(message='Задължително поле.')])
    email = EmailField('Email')
    tel = IntegerField('Телефон')
    date_of_reg = DateTimeField(default=datetime.now(), format="%d-%m-%Y")
    date_of_payment = DateTimeField(default=datetime.now(), format="%d-%m-%Y")
    user_id = StringField()
    submit = SubmitField('Запис')

    def __init__(self, *args, **kwargs):
        super(EditingCitizenForm, self).__init__(*args, **kwargs)
        self.position.choices = [('member', 'член'), ('chairmen', 'председател'),
                                 ('vice chairman', 'зам-председател'), ('secretary', 'секретар'),
                                 ('other', 'друга')]


class CitizenSearchForm(FlaskForm):
    id = IntegerField()
    egn = IntegerField('ЕГН', validators=[DataRequired(message='Задължително поле.')])
