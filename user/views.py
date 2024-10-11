import flask 

import flask_login

from .models import User

from main.settings import DATABASE

users = User.query.all()

def render_user():
    return flask.render_template(template_name_or_list = "user.html")

def render_registration():
    global users
    confirm = False
    if flask.request.method == "POST":
        name = flask.request.form["username"]
        password = flask.request.form["password"]
        try:
            is_user = False
            for user in users:
                if user.name == name and user.password == password:
                    is_user = True  
            if not is_user:
                confirm = True
                new_user = User(name = name, password = password)
                DATABASE.session.add(new_user)
                DATABASE.session.commit()
        except Exception as _ex:
            print(f"Error in func render registration \n\n{_ex}")
    return flask.render_template(template_name_or_list = "registration.html", confirm = confirm, link = "None")

def render_login():
    global users
    confirm = True
    if flask.request.method == "POST":
        confirm = False
        name = flask.request.form["username"]
        password = flask.request.form["password"]
        for user in users:
            if user.name == name and user.password == password:
                flask_login.login_user(user=user)
                return flask.redirect("/")
    return flask.render_template(template_name_or_list = "login.html", confirm = confirm, link = "None")