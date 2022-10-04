from django.apps import AppConfig

from apps.account.signals import password_reset_token_created


class AccountConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.account'

    def activate_signals(self):
        return password_reset_token_created
