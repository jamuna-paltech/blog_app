from shutil import Error
from urllib.parse import urlsplit
from app import app, users
from flask import render_template, flash, redirect, request, session, url_for
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from datetime import datetime, timezone

# @app.before_request
# def before_request():
#     if session.get("loggedInUser"):
#         session["loggedInUser"].last_seen = datetime.now(timezone.utc)

@app.route("/")
@app.route("/index")
def index():
    if not session.get('loggedInUser'):
        return redirect(url_for("login"))
    posts = [
        {
            "author": {"username": "Kenel"}, 
            "body": "post 1"
        },
        {
            "author": {"username": "Pankaj"}, 
            "body": "post 2"
        },
    ]
    return render_template("index.html", title="Home", posts=posts)

@app.route("/login", methods=["GET", "POST"])
def login():
    # if current_user.is_authenticated:
    #     return redirect(url_for("index"))
    
    form = LoginForm()
    if form.validate_on_submit():
        loggedInUser = None
        for user in users:
            if user['username']==form.username.data:
                loggedInUser = user
                break
        if loggedInUser is None or not loggedInUser["password"] == (form.password.data):
            flash('Invalid password or username.')
            return redirect(url_for("login"))
        # login_user(user, remember=form.remember_me.data)
        session["loggedInUser"] = loggedInUser
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            # the application only redirects when the URL is relative, which ensures that the redirect stays within the same site as the application. To determine if the URL is absolute or relative, I parse it with Python's urlsplit() function and then check if the netloc component is set or not.
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

@app.route("/logout")
def logout():
    session.pop("loggedInUser", None)
    return redirect(url_for("index"))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        newUser = {"id": users[len(users)-1]["id"]+1,"username": form.username.data, "email": form.email.data, "password": form.password.data}
        users.append(newUser)
        print("new user", newUser)
        flash('Congratulations, you are now a registered user!', newUser)
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<username>')
def user(username):
    if not session.get('loggedInUser'):
        return redirect(url_for("login"))
    user = None
    for u in users:
        if u['username']==username:
            user = u
            break
    if user is None:
        return Error("User not found")
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html', user=user, posts=posts)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if not session.get('loggedInUser'):
        return redirect(url_for("login"))
    form = EditProfileForm()
    if form.validate_on_submit():
        session["loggedInUser"].username = form.username.data
        session["loggedInUser"].about_me = form.about_me.data
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = session["loggedInUser"]["username"] or 'default'
        form.about_me.data = session["loggedInUser"]["about_me"] or ''
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


