from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from flask_mail import Mail, Message
from flask_wtf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
from forms import LoginForm, RegisterForm, ContactForm, EventForm
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
CSRFProtect(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)

class ContactMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/donations')
def donations():
    return render_template('donations.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        message_text = form.message.data
        record = ContactMessage(email=email, message=message_text)
        db.session.add(record)
        db.session.commit()
        try:
            msg = Message('New Contact Message', recipients=['djruiz44@gmail.com'])
            msg.body = f"From: {email}\n\n{message_text}"
            mail.send(msg)
            flash('Message sent!')
        except Exception:
            flash('Could not send email.')
        return redirect(url_for('contact'))
    return render_template('contact.html', form=form)

@app.route('/schedule')
    form = EventForm()
    return render_template('schedule.html', events=events, form=form)
@login_required
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            name=form.name.data,
            date=form.date.data.strftime('%Y-%m-%d'),
            description=form.description.data,
        )
        db.session.add(event)
        db.session.commit()
        flash('Event added')
    else:
        flash('Invalid input')
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
    return render_template('login.html', form=form)
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            hashed_pw = generate_password_hash(password)
            user = User(username=username, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(debug=debug, host='0.0.0.0', port=port)
    app.run(debug=True, host='0.0.0.0', port=port)
