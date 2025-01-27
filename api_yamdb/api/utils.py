import random
from django.core.mail import send_mail


def send_verification_email(user, code):
    subject = 'Верификация электронной почты'
    message = f'Ваш код подтверждения: {code}'
    send_mail(subject, message, 'from@example.com', [user.email])


def generate_verification_code():
    return random.randint(100000, 999999)
