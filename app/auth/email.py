import smtplib 
from flask import redirect, url_for

def send_email(subject, msg, receiver):
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.ehlo()
        server.starttls()
        server.login("rentalrecordimage@gmail.com", "rentalrecordimage1") 
        message = "Subject: {}\n\n{}".format(subject, msg) 
        server.sendmail("rentalrecordimage@gmail.com", receiver, message)
        server.quit()
    except:
        return redirect(url_for("auth.login"))

