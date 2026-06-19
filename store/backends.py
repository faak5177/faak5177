from django.contrib.auth.backends import BaseBackend
from store.models import User as StoreUser

class DatabaseBackend(BaseBackend):
    """Аутентификация через таблицу Users базы данных."""

    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            store_user = StoreUser.objects.get(login=username)
            if store_user.password == password:
                from django.contrib.auth.models import User as AuthUser
                auth_user, created = AuthUser.objects.get_or_create(
                    username=store_user.login,
                    defaults={
                        'first_name': store_user.first_name,
                        'last_name': store_user.last_name,
                        'email': store_user.login,
                    }
                )
                if created:
                    auth_user.set_unusable_password()
                    auth_user.save()
                return auth_user
        except StoreUser.DoesNotExist:
            return None
        return None

    def get_user(self, user_id):
        from django.contrib.auth.models import User as AuthUser
        try:
            return AuthUser.objects.get(pk=user_id)
        except AuthUser.DoesNotExist:
            return None
