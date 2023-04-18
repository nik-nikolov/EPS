from datetime import datetime, timedelta

import flask
import flask_login
import js2py
from flask import render_template, redirect, url_for, request, flash
from flask_login import current_user, logout_user, login_required, login_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm, RegistrationForm, EditingForm, CitizenForm, CitizenSearchForm, EditingCitizenForm
from app.models import User, Citizen, numbers_to_words


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = CitizenForm()
    if request.method == 'POST' and form.validate_on_submit():
        citizen = Citizen(name=form.name.data, surname=form.surname.data, family=form.family.data,
                          egn=form.egn.data, idcard=form.idcard.data, date_of_issue=form.date_of_issue.data,
                          issued_by=form.issued_by.data, position=form.position.data,
                          vote_section=form.vote_section.data,
                          sum=form.sum.data, email=form.email.data, tel=form.tel.data,
                          user_id=current_user.id, date_of_reg=datetime.now())
        try:
            _egn = str(form.egn.data)
            citizen.check_egn(_egn)  # check if egn is validated
            db.session.add(citizen)
            db.session.commit()
            db.session.close()
            print('Успешен запис')
            flash('Записът премина успешно!', category="success")
        except Exception as e:
            print(e)
            flash('Грешка при записа!', category="danger")
        return redirect(url_for('index'))
    return render_template('index.html', title='Home', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user0 = User.query.filter_by(username=form.username.data).first()
            if user0 is None or not user0.check_password(form.password.data):
                flash("Невярно потребителско име или парола", category="danger")
                return redirect(url_for('login'))
            login_user(user0, remember=form.remember_me.data)
            next_page = request.args.get('next')
            if not next_page or url_parse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        return redirect(url_for('login'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    form = RegistrationForm()
    if request.method == 'POST' and form.validate_on_submit():
        user1 = User(username=form.username.data, name=form.name.data, surname=form.surname.data,
                     family=form.family.data, email=form.email.data, role=form.role.data)
        user1.set_password(form.password.data)
        try:
            db.session.add(user1)
            db.session.commit()
            db.session.close()
            print('Успешна регистрация!')
            flash('Успешна регистрация!', category="success")
        except Exception as e:
            print(e)
            flash('Грешка при регистрация!', category="danger")
        return redirect(url_for('register'))
    return render_template('register.html', title='Register', form=form)


@app.route('/user', methods=['GET', 'POST'])
@login_required
def user():
    users = User.query.all()
    return render_template('user.html', users=users)


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit(id):
    user1 = User.query.get_or_404(id)  # execute the query with the primary-key and return an object or error 404
    form = EditingForm(obj=user1)
    form.populate_obj(user1)
    if request.method == 'POST' and form.validate_on_submit():
        try:
            list_username = db.session.query(User.username).all()
            if len(list_username) != len(set(list_username)):  # check if username is duplicate
                print("Have a duplicates")
                flash('Това потребителско име вече съществува.Моля въведете друго потребителско име')
                return render_template('edit_user.html', form=form, title='Editing')
            user1.set_password(form.password.data)
            db.session.merge(user1)
            db.session.flush()
            db.session.commit()
            db.session.close()
            print('Uspeh')
            flash('Записът премина успешно!', category="success")
        except Exception as e:
            print(e)
            flash('Грешка при записа!', category="danger")
        return redirect(url_for('user'))
    return render_template('edit_user.html', form=form, title='Editing')


@app.route('/delete/<int:id>')
@login_required
def delete(id):
    if current_user.role == 'user':
        return redirect(url_for('index'))
    try:
        user_del = User.query.get_or_404(id)
        db.session.delete(user_del)
        db.session.commit()
        flash('Успешно изтриване на данни !', category="success")
        return redirect(url_for('user'))
    except Exception as e:
        print(e)
        db.session.rollback()
        flash('Грешка при  изтриване на данни !', category="danger")
        return redirect(url_for('user'))


@app.route('/edit_c/<id>', methods=['GET', 'POST'])
@login_required
def edit_c(id=0):
    c = Citizen.query.get_or_404(id)
    _form = EditingCitizenForm(obj=c)
    _form.populate_obj(c)
    if request.method == 'POST' and _form.validate_on_submit():
        try:
            list_egn = db.session.query(Citizen.egn).all()
            if len(list_egn) != len(set(list_egn)):  # check if egn is duplicate
                print("Have a duplicates")
                flash('Този ЕГН вече съществува.Моля въведете друг ЕГН.')
                return render_template('edit_c.html', form=_form, title='Editing')
            _egn = str(c.egn)
            c.check_egn(_egn)
            c.date_of_reg = datetime.now()
            c.user_id = current_user.id
            db.session.merge(c)
            db.session.flush()
            db.session.commit()
            db.session.close()
            print('Uspeh')
            flash('Записът премина успешно!', category="success")
        except Exception as e:
            print(e)
            db.session.rollback()
            flash('Грешка при записа!', category="danger")
        return redirect(url_for('search'))
    return render_template('edit_c.html', form=_form, title='Editing_citizen')


@app.route('/search', methods=('GET', 'POST'))
@login_required
def search():
    _form = CitizenSearchForm()
    if request.method == 'POST':
        if _form.validate_on_submit():
            try:
                data = _form.egn.data
                c = Citizen.query.filter_by(egn=data)
                id = c[0].id
                return redirect(url_for('edit_c', id=id))
            except Exception as e:
                print('Несъществуващ ЕГН.Опитайте отново !', str(e))
                flash('Несъществуващ ЕГН.Опитайте отново !', category="danger")
        return redirect(url_for('search'))
    return render_template('search.html', form=_form, title='Search_citizen')


@app.route('/payment/<id>', methods=('GET', 'POST'))
@login_required
def payment(id):
    c = Citizen.query.get_or_404(id)
    form = CitizenForm(obj=c)
    # print(form.data)
    # if request.method == 'POST':
    t = datetime.now()
    today = t.strftime("%d/%m/%Y")
    with app.app_context():
        try:
            if form.date_of_payment.data:
                date = form.date_of_payment.data.strftime("%d-%m-%Yг. в %H ч. и %M мин. ")
                flash('Сумата на лицето' + " " + str(form.name.data) + " " + str(form.surname.data) + " " + str(
                    form.family.data) + " " +
                      'е била изплатена на ' + date + " " '!',
                      category="danger")
                return redirect(url_for('search'))
            else:
                name = form.name.data
                surname = form.surname.data
                family = form.family.data
                egn = str(form.egn.data)
                idcard = str(form.idcard.data)
                date_of_issue = form.date_of_issue.data
                date_of_issue = str(date_of_issue.strftime("%d/%m/%Y"))
                issued_by = form.issued_by.data
                vote_section = str(form.vote_section.data)
                c.date_of_payment = datetime.now()
                _sum = str(form.sum.data)
                suma = _sum.split('.')
                digit = int(suma[0])
                digit1 = suma[1]
                digit = (numbers_to_words(digit))  # convert digits to words

                data = "\n\
        =============================================================\n\
                Община ШУМЕН\n\n\t\tРазходен касов ордер\n\n\t\t№........дата г.\n\n\tДа се брои на:име бащино фамилия\n\n\
    ЕГН:егн лк №.номер изд.на:дат_изд г. от изд_от\n\n\tза учaстие в СИК № секном  сума:плащане лв.\n\n\
    с думи(текст)лв. и тстот ст.\n\n\n\t Гл.счет:........ Ръковод:......... Касиер:..........\n\n\t\t\t\t\
            /С.Еюбова/\n\n\tПолучил:.........Счетоводител:...........\n\n\t\t\t\t\t  /В.Христова/\n\n\
        =============================================================\n"
                data = data.replace('дата', today)
                data = data.replace('име', name)
                data = data.replace('бащино', surname)
                data = data.replace('фамилия', family)
                data = data.replace('егн', egn)
                data = data.replace('номер', idcard)
                data = data.replace('дат_изд', date_of_issue)
                data = data.replace('изд_от', issued_by)
                data = data.replace('секном', vote_section)
                data = data.replace('плащане', _sum)
                data = data.replace('текст', digit)
                data = data.replace('тстот', digit1)
                db.session.merge(c)
                db.session.flush()
                db.session.commit()
                with open("text.txt", mode='w+') as f:
                    f.write(data)
                    f.seek(0)
                    content = f.read()
                return render_template('payment.html', text=content, title='Payment')
        except Exception as e:
            db.session.rollback()
            print(e)
            flash('Грешка при  заплащане.Проверете връзката с принтера !', category="danger")
            # return redirect(url_for('payment', form=form, title='Payment')
            return render_template('payment_new.html', title='Payment')


@app.route('/printer', methods=('GET', 'POST'))
@login_required
def printer():
    # os.startfile('test.txt', "print")
    with open("text.txt", mode='r') as f:
        content = f.read()
        # print(content)
    try:
        js2py.eval_js('console.log("Hello World!")')
        js = """
        function printpage(content) {
         var text=content
    myWindow = window.open('', '', 'width=800,height=600');
    myWindow.innerWidth = screen.width;
    myWindow.innerHeight = screen.height;
    myWindow.screenX = 0;
    myWindow.screenY = 0;
    myWindow.document.body.innerHTML = text;
    myWindow.focus();
    }
    """
        context = js2py.eval_js('js(content)')
        context.execute(js)
        flash('Успешно изплатена сума', category="success")
        return redirect(url_for('search'))
    except Exception as e:
        print(str(e))
        flash('Грешка при  заплащане.Проверете връзката с принтера !', category="danger")
        return render_template('payment.html', title='Payment')


@app.route('/delete_c/<id>', methods=('GET', 'POST'))
@login_required
def delete_c(id):
    try:
        citizen_del = Citizen.query.get_or_404(id)
        db.session.delete(citizen_del)
        db.session.commit()
        flash('Успешно изтриване на данни !', category="success")
        return redirect(url_for('search'))
    except Exception as e:
        print(e)
        db.session.rollback()
        flash('Грешка при  изтриване на данни !', category="danger")
        return redirect(url_for('search'))


@app.before_request
def before_request():  # manage sessions.If empty 20 min. session is closed.
    flask.session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=20)
    flask.session.modified = True
    flask.g.user = flask_login.current_user
