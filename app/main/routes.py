from flask import render_template
from ..models import User
from . import main


@main.route('/')
def index():
    return render_template('main/index.html')


@main.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('main/user.html', user=user)

@main.route('/finduser')
def find_user():
    return render_template('main/finduser.html')


