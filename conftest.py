"""Pytest configuration: используем существующую demoekz.db (модели managed=False)."""
import os
import django
import pytest

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demoekz_project.settings')
django.setup()


@pytest.fixture(scope='session')
def django_db_setup():
    """Не создаём тестовую БД: модели managed=False, берём существующую demoekz.db."""
    pass


@pytest.fixture
def client():
    from django.test import Client
    return Client()


@pytest.fixture
def admin_credentials():
    """Администратор: Ворсин Пётр (Role_ID=1)."""
    return {'login': '94d5ous@gmail.com', 'password': 'uzWC67'}


@pytest.fixture
def manager_credentials():
    """Менеджер: Степанов Михаил (Role_ID=2)."""
    return {'login': '1diph5e@tutanota.com', 'password': '8ntwUp'}


@pytest.fixture
def client_credentials():
    """Авторизированный клиент: Михайлюк Анна (Role_ID=3)."""
    return {'login': '5d4zbu@tutanota.com', 'password': 'rwVDh9'}
