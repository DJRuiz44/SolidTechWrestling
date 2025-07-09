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
from forms import (
    LoginForm,
    RegisterForm,
    ContactForm,
    EventForm,
    ProfileForm,
    MatchForm,
)
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'change-me')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'localhost')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 25))
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@example.com')
CSRFProtect(app)

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)

user_colleges = db.Table(
    'user_colleges',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('college_id', db.Integer, db.ForeignKey('college.id')),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    graduation_year = db.Column(db.Integer)
    gpa = db.Column(db.Float)
    team = db.Column(db.String(150))
    school = db.Column(db.String(150))
    club = db.Column(db.String(150))
    height = db.Column(db.String(20))
    weight_class = db.Column(db.String(20))
    matches = db.relationship('Match', backref='user', lazy=True)
    colleges = db.relationship('College', secondary=user_colleges, backref='users')


class College(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    logo = db.Column(db.String(150))
    recruitment_url = db.Column(db.String(300))

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    opponent = db.Column(db.String(150), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)

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
    if not College.query.first():
        colleges = [
            College(
                name='State University',
                logo='state_university.svg',
                recruitment_url='https://example.com/state-form',
            ),
            College(
                name='City College',
                logo='city_college.svg',
                recruitment_url='https://example.com/city-form',
            ),
        ]
        db.session.add_all(colleges)
        db.session.commit()

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
def schedule():
    events = Event.query.order_by(Event.date).all()
    form = EventForm()
    return render_template('schedule.html', events=events, form=form)

@app.route('/add_event', methods=['POST'])
@login_required
def add_event():
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
    return redirect(url_for('schedule'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid credentials')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        if User.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            hashed_pw = generate_password_hash(password)
            user = User(username=username, password_hash=hashed_pw)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm(obj=current_user)
    form.colleges.choices = [(c.id, c.name) for c in College.query.all()]
    if request.method == 'GET':
        form.colleges.data = [c.id for c in current_user.colleges]
    if form.validate_on_submit():
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.graduation_year = form.graduation_year.data
        current_user.gpa = form.gpa.data
        current_user.team = form.team.data
        current_user.school = form.school.data
        current_user.club = form.club.data
        current_user.height = form.height.data
        current_user.weight_class = form.weight_class.data
        current_user.colleges = College.query.filter(College.id.in_(form.colleges.data)).all()
        db.session.commit()
        flash('Profile updated')
        return redirect(url_for('profile'))
    return render_template('profile.html', form=form)

@app.route('/matches', methods=['GET', 'POST'])
@login_required
def matches():
    form = MatchForm()
    if form.validate_on_submit():
        match = Match(
            user=current_user,
            opponent=form.opponent.data,
            date=form.date.data.strftime('%Y-%m-%d'),
            description=form.description.data,
        )
        db.session.add(match)
        db.session.commit()
        flash('Match added')
        return redirect(url_for('matches'))
    matches = Match.query.filter_by(user_id=current_user.id).order_by(Match.date).all()
    return render_template('matches.html', matches=matches, form=form)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() in ('1', 'true', 'yes')
    app.run(debug=debug, host='0.0.0.0', port=port)
