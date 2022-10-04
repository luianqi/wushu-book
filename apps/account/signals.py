from django.dispatch import receiver
from django.core.mail import send_mail

from django_rest_passwordreset.signals import reset_password_token_created


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    url = 'https://wushu-federation1.herokuapp.com/auth/NewPassword/'
    email_plaintext_message = "{}?token={}".format(url, reset_password_token.key)

    send_mail(
        # title:
        "Сброс пароля",
        # message:
        "Здравствуйте,\nДля сброса пароля Вашей учетной записи, перейдите по следующей ссылке: {}".format(email_plaintext_message),
        # from:
        "whushu.team1@gmail.com",
        # to:
        [reset_password_token.user.email]
    )
