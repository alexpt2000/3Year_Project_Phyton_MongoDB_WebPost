from flask import Flask, render_template, request, session, make_response, redirect, url_for

from common.database import Database
# from models.allPosts import AllPosts
from models.user import User


# deal with all flask activity , html page calls.
# secret key => a requirement from flask to allow the use of sessions
#  reference => http://flask.pocoo.org/docs/0.11/quickstart/#sessions
app = Flask(__name__)
app.secret_key = 'GMITblog'


# Home Page
@app.route('/')
def home_init():
    posts = User.from_mongo()
    return render_template('index.html', posts=posts)


# Login Page
@app.route('/login')
def login_init():
    return render_template('login.html')


# Register Page
@app.route('/register')
def register_init():
    return render_template('register.html')


# initialize the database
@app.before_first_request
def database_initialize():
    Database.initialize()


# Authenticate user login
@app.route('/authlogin', methods=['POST'])
def login_user():
    email = request.form['email']
    password = request.form['password']
    if User.login_valid(email, password):
        User.login(email)

    else:
        session['email'] = None

    user = User.get_by_email(session['email'])

    return render_template("profile.html", email=session['email'])
    return redirect(url_for('home_init'))


# Authenticate user register
@app.route('/authregister', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']

    User.register(name, email, password)

    user = User.get_by_email(session['email'])
    posts = user.get_posts()

    return render_template('user_posts.html', posts=posts, email=user.email)


# Show author's blog
@app.route('/posts/<string:user_id>')
@app.route('/posts')
def show_users_post(user_id=None):
    if user_id is not None:
        user = User.get_by_id(user_id)
    else:
        user = User.get_by_email(session['email'])
    posts = user.get_posts()

    return render_template('user_posts.html', posts=posts, email=user.email, name=user.name)


# Create and show blog
@app.route('/postsnew', methods=['POST', 'GET'])
def create_blog():
    if request.method == 'GET':
        return render_template('new_post.html')
    else:
        title = request.form['title']
        description = request.form['description']
        user = User.get_by_email(session['email'])
        user.new_post(title, description)
        return make_response(show_users_post(user._id))


# Log out
@app.route('/logout')
def logout():
    session['email'] = None
    return render_template('logout.html')


if __name__ == '__main__':
    app.run(port=4990, debug=True)

