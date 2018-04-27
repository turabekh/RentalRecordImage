from flask import render_template, request, flash, redirect, url_for
import os
import random
from ..models import User, Checkin, Checkout, Message
from . import dashboard 
from flask_login import current_user, login_required
from .forms import CheckinForm, CheckoutForm, CheckoutStartForm, ConfirmForm, SendLinkForm
from .images import resize_image
from ..import APP_ROOT, db
from .email import send_email






@dashboard.route('/')
def index():
    return render_template('dashboard/index.html')

@dashboard.route('/newcheckin', methods=["GET", "POST"])
@login_required
def new_checkin():
    form = CheckinForm()
    if form.validate_on_submit():
        car_number = form.car_number.data 
        agent_name = form.agent_name.data 
        add_info = form.add_info.data
         
        target = os.path.join(APP_ROOT, 'images/')
        if not os.path.isdir(target):
            os.mkdir(target)
        photo_list = dict()
        counter = 1
        if len(request.files.getlist("file")) != 6:
            flash("Please upload 6(six) photos of the vehicle")
            return redirect(url_for("dashboard.new_checkin"))
        for file in request.files.getlist("file"):
            filename = current_user.username + str(random.randint(1, 100000))+".jpg"
            destination = "/".join([target, filename])
            entry = "photo_" + str(counter)
            photo_list[entry] = filename
            counter = counter + 1
            file.save(destination)
            try:
                resize_image(200, 200, destination)
            except:
                continue
        photo_1 = photo_list.get("photo_1")
        photo_2 = photo_list.get("photo_2")
        photo_3 = photo_list.get("photo_3")
        photo_4 = photo_list.get("photo_4")
        photo_5 = photo_list.get("photo_5")
        photo_6 = photo_list.get("photo_6")
        checkin = Checkin(car_number = car_number, agent_name = agent_name, add_info = add_info, 
                          photo_1 = photo_1, photo_2 = photo_2, photo_3 = photo_3, photo_4 = photo_4,
                          photo_5 = photo_5, photo_6 = photo_6, customer = current_user)
        db.session.add(checkin)
        db.session.commit()
        flash("New case has been created succesfully")
        return redirect(url_for("dashboard.index"))
    return render_template("dashboard/newcheckin.html", form=form)


@dashboard.route('/newcheckout', methods=["GET", "POST"])
@login_required
def new_checkout():
    form = CheckoutForm()
    try:
        #car_number = request.args['car_number']
        if form.validate_on_submit():
            car_number = form.car_number.data 
            agent_name = form.agent_name.data 
            add_info = form.add_info.data
            
            target = os.path.join(APP_ROOT, 'images/')
            if not os.path.isdir(target):
                os.mkdir(target)
            photo_list = dict()
            counter = 1
            if len(request.files.getlist("file")) != 6:
                flash("Please upload 6(six) photos of the vehicle")
                return redirect(url_for("dashboard.new_checkout"))
            for file in request.files.getlist("file"):
                filename = current_user.username + str(random.randint(1, 100000))+".jpg"
                destination = "/".join([target, filename])
                entry = "photo_" + str(counter)
                photo_list[entry] = filename
                counter = counter + 1
                file.save(destination)
                try:
                    resize_image(200, 200, destination)
                except:
                    continue
            photo_1 = photo_list.get("photo_1")
            photo_2 = photo_list.get("photo_2")
            photo_3 = photo_list.get("photo_3")
            photo_4 = photo_list.get("photo_4")
            photo_5 = photo_list.get("photo_5")
            photo_6 = photo_list.get("photo_6")
            checkout = Checkout(car_number = car_number, agent_name = agent_name, add_info = add_info, 
                            photo_1 = photo_1, photo_2 = photo_2, photo_3 = photo_3, photo_4 = photo_4,
                            photo_5 = photo_5, photo_6 = photo_6, customer = current_user)
            db.session.add(checkout)
            db.session.commit()
            flash("New case has been created succesfully")
            return redirect(url_for("dashboard.index"))
        return render_template("dashboard/newcheckout.html", form=form, car_number=request.args['car_number'])
    except:
        return render_template("dashboard/newcheckout.html", form=form)
   






@dashboard.route('/startcheckout', methods = ["GET", "POST"])
@login_required
def checkout_start():
    form = CheckoutStartForm()
    if form.validate_on_submit():       
        car_number = form.car_number.data  
        user = User.query.filter_by(id=current_user.id).first_or_404()
        if user:
            checkins = user.checkins.order_by(Checkin.created_at.desc()).all() 
            if checkins:

                for checkin in checkins:
                    if car_number != checkin.car_number:
                        car = None
                        continue 
                    else:
                        car = checkin 
                        break 
                if car:
                    flash("Record has been found for this car number")
                    return redirect(url_for("dashboard.new_checkout", car_number = car.car_number))
                else:
                    flash("No pickup record found for this case")
                    return redirect(url_for("dashboard.confirm"))
            flash("No records found for this entry")
            return redirect(url_for("dashboard.confirm"))
            
    return render_template("dashboard/startcheckout.html", form = form)


@dashboard.route("/confirm", methods = ["GET", "POST"])
@login_required
def confirm():
    form = ConfirmForm()
    if form.validate_on_submit():
        yes = form.yes.data 
        no = form.no.data 
        if yes:
            return redirect(url_for("dashboard.new_checkout", car_number = ""))
        if no: 
            flash("The process has been cancelled")
            return redirect(url_for("dashboard.index"))
    return render_template("dashboard/confirm.html", form=form)



@dashboard.route('/mycases')
@login_required
def mycases():
    user = User.query.filter_by(id=current_user.id).first_or_404()
    user_checkins = user.checkins.order_by(Checkin.created_at.desc()).all()
    user_checkouts = user.checkouts.order_by(Checkout.created_at.desc()).all()
    return render_template("dashboard/mycases.html", user_checkins = user_checkins, user_checkouts = user_checkouts)


@dashboard.route("/message")
@login_required
def message():
    user = User.query.filter_by(id=current_user.id).first_or_404()
    user_messages = user.messages.order_by(Message.created_at.desc()).all()
    return render_template("dashboard/message.html", user_messages = user_messages)

@dashboard.route('/showcheckin/<int:id>')
def show_checkin(id):
    checkin = Checkin.query.filter_by(id=id).first_or_404()

    return render_template("dashboard/_checkin_header.html", checkin = checkin)

@dashboard.route('/showcheckout/<int:id>')
def show_checkout(id):
    checkout = Checkout.query.filter_by(id=id).first_or_404()

    return render_template("dashboard/_checkout_header.html", checkout = checkout)


@dashboard.route("/deletecheckin/<int:id>")
@login_required
def delete_checkin(id):
    checkin = Checkin.query.filter_by(id=id).first_or_404()
    if checkin:
        db.session.delete(checkin)
        db.session.commit()
        flash("A record has been deleted")
        return redirect(url_for("dashboard.mycases"))
    flash("Something went wrong. A record was not deleted. Try again")
    return redirect(url_for("dashboard.mycases"))


@dashboard.route("/deletecheckout/<int:id>")
@login_required
def delete_checkout(id):
    checkout = Checkout.query.filter_by(id=id).first_or_404()
    if checkout:
        db.session.delete(checkout)
        db.session.commit()
        flash("A record has been deleted")
        return redirect(url_for("dashboard.mycases"))
    flash("Something went wrong. A record was not deleted. Try again")
    return redirect(url_for("dashboard.mycases"))


@dashboard.route('/sendlink', methods=['GET', 'POST'])
def send_link():
    form= SendLinkForm()
    if form.validate_on_submit():
        receiver_email = form.email.data 
        url = form.record_url.data 
        send_email("Rental Record Photos/Info", url, receiver_email)
        flash("Email has been sent. Thanks")
        return redirect(url_for("dashboard.index"))
    return render_template("dashboard/sendlink.html", form=form)