#!/usr/bin/env python3
"""Восстанавливает Django-скобки в шаблонах. Запустите раз после clone.

  python setup_django.py
"""
import os

LBRC = chr(123) * 2
RBRC = chr(125) * 2
LT = "__LBRC__"
RT = "__RBRC__"
EXTS = (".html", ".py", ".md", ".txt", ".css", ".js")

changed = 0
for dirpath, _, files in os.walk('.'):
    for fn in files:
        if not fn.endswith(EXTS):
            continue
        full = os.path.join(dirpath, fn)
        try:
            with open(full, 'r', encoding='utf-8') as f:
                data = f.read()
        except (UnicodeDecodeError, OSError):
            continue
        if LT in data or RT in data:
            new = data.replace(LT, LBRC).replace(RT, RBRC)
            with open(full, 'w', encoding='utf-8') as f:
                f.write(new)
            print(f'restored: {full}')
            changed += 1
print(f'done. files restored: {changed}')
