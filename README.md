# Демоэкзамен — Продажа стройматериалов (вариант 3, профильный)

Проект по демоэкзамену 09.02.07-2-2026-ПУ — информационная система для продажи стройматериалов.

## Стек

- **Python 3.10+**
- **Django 4.2+**
- **SQLite 3** (`demoekz.db` в корне проекта)
- **Pillow** — масштабирование фото до 300×200

## Быстрый старт

```bash
python -m venv venv
source venv/bin/activate     # или venv\Scripts\activate на Windows
pip install -r requirements.txt

python setup_django.py             # ВАЖНО: восстанавливает Django-скобки в шаблонах (одноразово)
python manage.py migrate
python manage.py create_orders_table   # создаёт все таблицы managed=False
python manage.py import_data          # импорт из CSV
python manage.py runserver
```

Открыть в браузере: <http://127.0.0.1:8000/>

## Учётные записи

| Роль | Логин | Пароль |
|------|-------|--------|
| Администратор | `94d5ous@gmail.com` | `uzWC67` |
| Менеджер      | `1diph5e@tutanota.com` | `8ntwUp` |
| Клиент        | `5d4zbu@tutanota.com`  | `rwVDh9` |
| Гость         | — (кнопка «Гостевой режим») | — |

## Структура БД (3НФ)

- `Roles`, `Users`, `Category`, `Manufactures`, `Suplyers`, `Products`, `Pickups`, `Orders`
- ER-диаграмма: `docs/ER_diagram.pdf` / `.png`
- UML use-case: `docs/UseCase_diagram.pdf` / `.png`
- Блок-схема алгоритма авторизации: `docs/algorithm_flowchart.pdf` / `.png`

## Вариативная часть (профиль)

- `backup/demoekzamen_backup_2026-06-19.db` — бинарный бэкап
- `backup/demoekzamen_backup_2026-06-19.sql` — SQL-дамп
- `docs/disk_usage_report.docx` — отчёт по месту на диске
- `docs/test_scenarios.docx` — тестовые сценарии по ролям
