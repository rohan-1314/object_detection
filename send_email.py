import smtplib
from email.message import EmailMessage
import imghdr
import os

PASSWORD = os.getenv('PASSWORD')
SENDER = 'rohan.vagadiya14@gmail.com'


def send_email(img_path, reciever):
    email_message = EmailMessage()
    email_message['subject'] = 'An object was detected'
    email_message.set_content('A person or some object was detected!')
    with open(img_path, 'rb') as file:
        content = file.read()
    email_message.add_attachment(content, maintype='image',
                                 subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP('smtp.gmail.com', 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, reciever, email_message.as_string())
    gmail.quit()
    print('email sent')
