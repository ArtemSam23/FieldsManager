import smtplib
from email.message import EmailMessage
import os


# Setting environment variables
EMAIL_HOST = 'smtp.yandex.ru' #os.environ['EMAIL_HOST']
EMAIL_PORT = 465#int(os.environ['EMAIL_PORT'])
EMAIL_USER = 'no-reply@aerospace-agro.com' # os.environ['EMAIL_USER']
EMAIL_PASS = 'fo2yoks2eX1gRDpv' #os.environ['EMAIL_PASS']
#AWS_ACCESS_KEY_ID=AKIAYLFAQQNY5PJ3YW7S;AWS_SECRET_ACCESS_KEY=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;AWS_DEFAULT_REGION=us-west-2;EMAIL_HOST=smtp.yandex.ru;EMAIL_PORT=465;EMAIL_USER=no-reply@aerospace-agro.com;EMAIL_PASS=fo2yoks2eX1gRDpv;SECRET_TOKEN_KEY=bbc23a0560c592bb3e15aea3ee03479f04b142b711bb18ce0b476cc>;TOKEN_ALGORITHM=HS256

def send_code(email: str, code: str):
    message = EmailMessage()
    message['Subject'] = "Confirm your email"
    message['From'] = EMAIL_USER
    message['To'] = email
    message.set_content(f'Your code: {code}')
    with smtplib.SMTP_SSL(host=EMAIL_HOST, port=EMAIL_PORT) as s:
        s.login(user=EMAIL_USER, password=EMAIL_PASS)
        s.send_message(message)


def send_signup_confirmation(email: str):
    message = EmailMessage()
    message['Subject'] = "Signup confirmation"
    message['From'] = EMAIL_USER
    message['To'] = email
    message.set_content("You have been signed up.")
    with smtplib.SMTP_SSL(host=EMAIL_HOST, port=EMAIL_PORT) as s:
        s.login(user=EMAIL_USER, password=EMAIL_PASS)
        s.send_message(message)

def send_notification(title: str, description: str, email: str):
    message = EmailMessage()
    message['Subject'] = title
    message['From'] = EMAIL_USER
    message['To'] = email
    message.set_content(f"{description}")
    with smtplib.SMTP_SSL(host=EMAIL_HOST, port=EMAIL_PORT) as s:
        s.login(user=EMAIL_USER, password=EMAIL_PASS)
        s.send_message(message)
