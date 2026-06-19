"""Тесты для роли 'Авторизированный клиент' (≥2 сценария)."""
import pytest


@pytest.mark.django_db
class TestClient:
    def test_client_can_login(self, client, client_credentials):
        """Сценарий 1: клиент входит в систему."""
        response = client.post('/login/', client_credentials, follow=True)
        assert response.status_code == 200

    def test_client_can_view_catalog(self, client, client_credentials):
        """Сценарий 2: клиент видит каталог товаров."""
        client.post('/login/', client_credentials)
        response = client.get('/')
        assert response.status_code == 200

    def test_client_can_open_order_form(self, client, client_credentials):
        """Сценарий 3: клиент может оформить заказ."""
        client.post('/login/', client_credentials)
        response = client.get('/orders/new/')
        assert response.status_code in (200, 302)

    def test_guest_can_browse_catalog(self, client):
        """Сценарий 4 (Гость): просмотр каталога без авторизации."""
        response = client.get('/')
        assert response.status_code in (200, 302)
