from django.conf import settings
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.urls import get_resolver
from django.utils import timezone

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP
from threading import Thread
from base64 import urlsafe_b64decode, urlsafe_b64encode
from binascii import Error as b64Error


from user.errors import InvalidUserModel, EmailTemplateNotFound, NotAllFieldCompiled


def sendResetPasswordEmail(user, **kwargs):
    try:

        try:
            token = kwargs['token']
        except KeyError:
            token = default_token_generator.make_token(user)

        email = urlsafe_b64encode(str(user.email).encode('utf-8'))

        t = Thread(target=resetPasswordThread, args=(user.username, user.email, f'/{email.decode("utf-8")}/{token}'))
        t.start()
    except AttributeError:
        raise InvalidUserModel('The user model you provided is invalid')


def resetPasswordThread(username, email, token):
    email_server = validateAndGetField('EMAIL_SERVER')
    sender       = validateAndGetField('EMAIL_FROM_ADDRESS')
    domain       = validateAndGetField('EMAIL_RESET_PASSWORD_DOMAIN')
    subject      = validateAndGetField('EMAIL_RESET_PASSWORD_SUBJECT')
    address      = validateAndGetField('EMAIL_ADDRESS')
    port         = validateAndGetField('EMAIL_PORT', default_type=int)
    password     = validateAndGetField('EMAIL_PASSWORD')
    mail_html    = validateAndGetField('EMAIL_RESET_PASSWORD_HTML', raise_error=False)

    if not (mail_html):  # Validation for mail_plain and mail_html as both of them have raise_error=False
        raise NotAllFieldCompiled(f"Both EMAIL_MAIL_PLAIN and EMAIL_MAIL_HTML missing from settings.py, at least one of them is required.")

    domain += '/' if not domain.endswith('/') else ''

    msg            = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From']    = sender
    msg['To']      = email

    from .views import confirmEmail
    link = domain + username + token
    print(link)
    for k, v in get_resolver(None).reverse_dict.items():
        if k is confirmEmail and v[0][0][1][0]:
            addr = str(v[0][0][0])
            link = domain + addr[0: addr.index('%')] + token

    if mail_html:
        try:
            html = render_to_string(mail_html, {'link': link})
            part2 = MIMEText(html, 'html')
            msg.attach(part2)
        except AttributeError:
            pass

    if not msg.get_payload():
        raise EmailTemplateNotFound('No email template found')

    server = SMTP(email_server, port)
    server.starttls()
    server.login(address, password)
    server.sendmail(sender, email, msg.as_string())
    server.quit()


def validateAndGetField(field, raise_error=True, default_type=str):
    try:
        d = getattr(settings, field)
        if d == "" or d is None or not isinstance(d, default_type):
            raise AttributeError
        return d
    except AttributeError:
        if raise_error:
            raise NotAllFieldCompiled(f"Field {field} missing or invalid")
        return None


def verifyToken(email, email_token):
    try:
        users = get_user_model().objects.filter(email=urlsafe_b64decode(email).decode("utf-8"))
        for user in users:
            valid = default_token_generator.check_token(user, email_token)
            if valid:
                return True
    except b64Error:
        pass
    return False
