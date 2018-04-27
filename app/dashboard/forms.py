from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.fields.html5 import DateField
from wtforms.validators import Optional, Length, Required, URL, Email
from flask_wtf.file import FileField, FileAllowed, FileRequired


class CheckinForm(FlaskForm):
    car_number = StringField("Car Number", validators=[Required(), Length(1, 128)])
    agent_name = StringField("Agent Name", validators=[Optional(), Length(1, 50)])
    add_info = TextAreaField("Additional Info")
    submit = SubmitField("Submit")



class CheckoutForm(FlaskForm):
    car_number = StringField("Car Number", validators=[Required(), Length(1, 128)])
    agent_name = StringField("Agent Name", validators=[Optional(), Length(1, 50)])
    add_info = TextAreaField("Additional Info")
    submit = SubmitField("Submit")

class CheckoutStartForm(FlaskForm):
    car_number = StringField("Car Number", validators=[Required(), Length(1, 50)])
    find_checkin = SubmitField("Find Record")


class ConfirmForm(FlaskForm):
    yes = SubmitField("Continue without rental pick up information")
    no = SubmitField("Cancel")


class SearchFormByDate(FlaskForm):
    date = DateField("Enter Date")
    find = SubmitField("Find a Record")

class  SearchForm(FlaskForm):
    car_number = StringField("Car Number", validators=[Required()])
    find = SubmitField("Search")

class  SendLinkForm(FlaskForm):
    email = StringField("Receiver's Email", validators=[Required(), Length(1, 64), Email()])
    record_url = StringField('Record URL',
                            validators=[Length(1, 128), URL()])
    send = SubmitField("Send Email")
