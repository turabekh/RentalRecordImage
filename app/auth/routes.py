from flask import render_template, current_app, request, redirect, url_for, \
    flash
from flask_login import login_user, logout_user, login_required, current_user
from ..models import User
from . import auth
from .forms import LoginForm, SignUpForm, ProfileForm, PasswordChangeForm, SendLinkForm
from ..import db
import app
from .email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if not current_app.config['DEBUG'] and not current_app.config['TESTING'] \
            and not request.is_secure:
        return redirect(url_for('.login', _external=True, _scheme='https'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.verify_password(form.password.data):
            flash('Invalid email or password.')
            return redirect(url_for('.login'))
        login_user(user, form.remember_me.data)
        return redirect(request.args.get('next') or url_for('dashboard.index'))
    return render_template('auth/login.html', form=form)



@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))



@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if not current_app.config['DEBUG'] and not current_app.config['TESTING'] \
        and not request.is_secure:
         return redirect(url_for('.login', _external=True, _scheme='https'))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash("Email Already exists. Please go to login")
            redirect("auth.signup")
        else:
            user = User.query.filter_by(username = form.username.data).first()
            if user:
                flash("Username already exists. Please user different username")
            else:
                try:
                    email = form.email.data
                    username = form.username.data  
                    password = form.password.data  
                    if (form.role.data):
                        role = form.role.data
                    else:
                        role = False
                    user = User(email=email, username=username, password=password, is_agent = role) 
                    db.session.add(user)
                    db.session.commit()
                    send_email("Thanks from RentalRecordImage", "You have been signed up successfully")
                    flash("Thanks. You have been signed up successfully")
                    return redirect(url_for("auth.login"))
                except:
                    flash("Sorry. Something went wrong. Please try again")
                    return redirect(url_for("auth.signup"))
    return render_template('auth/signup.html', form=form)


@auth.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.bio = form.bio.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('main.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.bio.data = current_user.bio
    return render_template('auth/profile.html', form=form)


@auth.route("/passwordprocess/<email>", methods=["GET", "POST"]) 
def process_password(email):
    form = PasswordChangeForm() 
    user = User.query.filter_by(email=email).first()
    if user:
        if form.validate_on_submit():
            user.password = form.password.data
            db.session.commit()
            flash("Your password has been reset")
            send_email("Success: Password Reset", "Your password has been reset successfully", user.email)
            logout_user()
            return redirect(url_for('auth.login'))
    return render_template("auth/passwordreset.html", form=form)

@auth.route("/sendpassowrdlink", methods=["GET", "POST"])
def send_link():
    form = SendLinkForm() 
    if form.validate_on_submit():
        email = form.email.data 
        link = "http://localhost:5000/auth/passwordprocess/"+email
        send_email("Password Reset", link, email)
        flash("Link to reset password has been sent to the email you have provided. Please check your email")
        return redirect(url_for("auth.login"))
    return render_template("auth/sendlinkform.html", form=form)
