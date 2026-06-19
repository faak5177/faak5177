"""Тесты для роли 'Менеджер' (≥2 сценария)."""
import pytest


@pytest.mark.django_db
class TestManager:
    def test_manager_can_login(self, client, manager_credentials):
        """Сценарий 1: менеджер входит в систему."""
        response = client.post('/login/', manager_credentials, follow=True)
        assert response.status_code == 200

    def test_manager_can_view_orders(self, client, manager_credentials):
        """Сценарий 2: менеджер видит список заказов."""
        client.post('/login/', manager_credentials)
        response = client.get('/orders/')
        assert response.status_code == 200

    def test_manager_sees_product_catalog(self, client, manager_credentials):
        """Сценарий 3: менеджер видит каталог товаров."""
        client.post('/login/', manager_credentials)
        response = client.get('/')
        assert response.status_code == 200
