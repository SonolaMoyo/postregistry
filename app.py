from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

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


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == "moyo@veo.com" and form.password.data == 'password':
            flash("You have been logged in!", 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Check credentials', 'danger')
    return render_template('login.html', title='Login', form=form)


db.create_all()
db.drop_all()
db.create_all()
user1 = User(username='John', email='john@gmail.com', password='john')
user2 = User(username='Sam', email='sam@gmail.com', password='sam')
user3 = User(username='Bill', email='bill@gmail.com', password="bill")
db.session.add(user1)
db.session.add(user2)
db.session.add(user3)
db.session.commit()

post1 = Post(title='Post11', content='John first post', user_id=user1.id)
post2 = Post(title='Post12', content='Sam first post', user_id=user2.id)
post3 = Post(title='Post13', content='Bill first post', user_id=user3.id)
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)
db.session.commit()

if __name__ == '__main__':
    app.run(port=3000, debug=True)
