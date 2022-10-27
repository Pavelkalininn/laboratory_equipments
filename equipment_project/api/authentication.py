from django.contrib.auth import get_user_model
from rest_framework import authentication, exceptions

User = get_user_model()


class BotAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        telegram_id = request.data.get('telegram_id')

        if not telegram_id:
            return None

        try:
            user = User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')
        return user, None
