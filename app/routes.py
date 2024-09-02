from shutil import Error
from urllib.parse import urlsplit
from flask_login import current_user, login_required, login_user, logout_user
from app import app, db, auth
from flask import render_template, flash, redirect, request, session, url_for
from app.forms import EditProfileForm, LoginForm, RegistrationForm
from datetime import datetime, timezone
import sqlalchemy as sa
from app.models import User
from config import Config

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.now(timezone.utc)
        db.session.commit()

@app.route("/")
@app.route("/index")
@login_required
def index():
    # posts = [
    #     {"author": {"username": "Kenel"}, "body": "post 1"},
    #     {"author": {"username": "Pankaj"}, "body": "post 2"},
    # ]
    posts = db.session.scalars(current_user.get_all_posts())
    return render_template("index.html", title="Home", posts=posts)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        loggedInUser = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        if loggedInUser is None or not loggedInUser.check_password(form.password.data):
            flash("Invalid password or username.")
            return redirect(url_for("login"))
        login_user(loggedInUser, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or urlsplit(next_page).netloc != "":
            # the application only redirects when the URL is relative, which ensures that the redirect stays within the same site as the application. To determine if the URL is absolute or relative, I parse it with Python's urlsplit() function and then check if the netloc component is set or not.
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form, **auth.log_in(
        scopes=Config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=url_for("auth_response", _external=True)
    ))


@app.route("/logout")
def logout():
    if session.get("access_token"):
        return redirect(auth.log_out(url_for("index", _external=True)))
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        u = User(username=form.username.data, email=form.email.data)
        u.set_password(password=form.password.data)
        print("new user", u)
        db.session.add(u)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


@app.route("/user/<username>")
@login_required
def user(username):
    user = db.first_or_404(sa.select(User).where(User.username == username))
    posts = db.session.scalars(current_user.get_posts())
    return render_template("user.html", user=user, posts=posts)


@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("edit_profile"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template("edit_profile.html", title="Edit Profile", form=form)

@app.route(Config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    print("result",result,loggedInUser)
    loggedInUser = db.session.scalar(sa.select(User).where(User.username == result.get("preferred_username")))
    if loggedInUser:
        login_user(loggedInUser, remember=False)
    else:
        user = User(username=result.get("preferred_username"), email=result.get("preferred_username"))
        db.session.add(user)
        db.session.commit()
        login_user(user, remember=False)
    if "error" in result:
        return render_template("500.html")
    return redirect(url_for("index"))
