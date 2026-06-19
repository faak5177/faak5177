from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User as AuthUser
from store.models import User as StoreUser

class StoreUserBackend(BaseBackend):
    """Кастомный backend: логин/пароль проверяются по таблице Users в БД магазина.
    При успешной проверке создаётся/синхронизируется AuthUser Django по полю username=login."""
    def authenticate(self, request, username=None, password=None, **kwargs):
        if not username or not password:
            return None
        try:
            store_user = StoreUser.objects.get(login=username, password=password)
        except StoreUser.DoesNotExist:
            return None
        auth_user, created = AuthUser.objects.get_or_create(
            username=store_user.login,
            defaults={
                'first_name': store_user.first_name,
                'last_name': store_user.last_name,
                'is_staff': store_user.role_id == 1,
                'is_superuser': store_user.role_id == 1,
            },
        )
        return auth_user

    def get_user(self, user_id):
        try:
            return AuthUser.objects.get(pk=user_id)
        except AuthUser.DoesNotExist:
            return None
