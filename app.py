from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)


# created a user class
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    password = db.Column(db.String(36), nullable=False)
    image = db.Column(db.String(20), nullable=False, default='pic.jpg')
    email = db.Column(db.String(50), unique=True, nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f'User("{self.username}", "{self.email}", "{self.image}")'

#created a post class
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'Post("{self.title}", "{self.date_posted}")'


posts = [
    {
        'author': 'Sonola Moyosoluwalorun',
        'title': 'Post 1',
        'content': 'Fullstack Software developer',
        'date_posted': 'September 30, 2022'
    },
{
        'author': 'Moyosoluwalorun Odunayo',
        'title': 'Post 2',
        'content': 'Data Scientist and Machine Learning Expert',
        'date_posted': 'October 30, 2022'
    },
{
        'author': 'Sonola Moyosoluwalorun Odunayo',
        'title': 'Post 3',
        'content': 'Cloud Engineer',
        'date_posted': 'November 30, 2022'
    }
]


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created! Username: {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


if __name__ == '__main__':
    app.run(port=3000, debug=True)
