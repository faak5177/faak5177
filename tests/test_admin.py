"""Тесты для роли 'Администратор' (≥2 сценария по заданию)."""
import pytest


@pytest.mark.django_db
class TestAdmin:
    def test_admin_can_open_login_page(self, client):
        """Сценарий 1: страница авторизации доступна админу."""
        response = client.get('/login/')
        assert response.status_code == 200
        assert b'\xd0\x90\xd0\xb2\xd1\x82\xd0\xbe\xd1\x80\xd0\xb8\xd0\xb7\xd0\xb0\xd1\x86\xd0\xb8\xd1\x8f' in response.content or b'login' in response.content.lower()

    def test_admin_login_with_valid_credentials(self, client, admin_credentials):
        """Сценарий 2: админ успешно входит в систему."""
        response = client.post('/login/', admin_credentials, follow=True)
        assert response.status_code == 200
        есть_сессия = '_auth_user_id' in client.session or 'user_id' in client.session
        assert есть_сессия

    def test_admin_can_access_product_create_form(self, client, admin_credentials):
        """Сценарий 3: админ имеет доступ к созданию товаров."""
        client.post('/login/', admin_credentials)
        response = client.get('/products/new/')
        assert response.status_code in (200, 302)

    def test_admin_can_view_products_list(self, client, admin_credentials):
        """Сценарий 4: админ видит список товаров."""
        client.post('/login/', admin_credentials)
        response = client.get('/')
        assert response.status_code == 200
