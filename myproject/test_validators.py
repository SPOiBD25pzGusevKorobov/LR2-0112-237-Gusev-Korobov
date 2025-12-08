#!/usr/bin/env python

import os
import sys
import django

# Настройка Django перед импортом моделей
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

# Теперь можно импортировать модели
from bboard.models import Product
from django.core.exceptions import ValidationError

print("=" * 70)
print("ДЕМОНСТРАЦИЯ СТАНДАРТНЫХ ВАЛИДАТОРОВ DJANGO")
print("=" * 70 + "\n")

# Создание с валидацией
print("1. Создание товара с валидными данными:")
try:
    product = Product(
        name='Телефон',
        supplier_email='test@example.com',
        product_url='https://example.com/product/1',
        price=15000.00,
        quantity=5,
        supplier_phone='+79991234567',
        article='AB123456',
        discount_percent=10
    )
    product.full_clean()  # Вызов валидации
    product.save()  # Сохранение
    print(f"   ✓ Товар успешно создан: {product.name}, цена: {product.price} руб.")
except ValidationError as e:
    print(f"   ✗ Ошибка валидации: {e.message_dict}")  # Вывод ошибок

print("\n" + "=" * 70 + "\n")

# Тест с неверными данными
print("2. Тест валидаторов с неверными данными:\n")

# Тест MinLengthValidator
print("   Тест MinLengthValidator (название < 3 символов):")
try:
    product2 = Product(
        name='AB',  # Слишком короткое
        supplier_email='test@example.com',
        price=1000.00,
        quantity=5,
        article='CD789012'
    )
    product2.full_clean()
    print("      ✗ Ошибка: валидация должна была провалиться")
except ValidationError as e:
    print(f"      ✓ Валидатор сработал: {e.message_dict.get('name', [''])[0]}")

# Тест MinValueValidator
print("\n   Тест MinValueValidator (цена < 0.01):")
try:
    product3 = Product(
        name='Тестовый товар',
        supplier_email='test@example.com',
        price=-100.00,  # Отрицательная цена
        quantity=5,
        article='EF345678'
    )
    product3.full_clean()
    print("      ✗ Ошибка: валидация должна была провалиться")
except ValidationError as e:
    print(f"      ✓ Валидатор сработал: {e.message_dict.get('price', [''])[0]}")

# Тест EmailValidator
print("\n   Тест EmailValidator (неверный email):")
try:
    product4 = Product(
        name='Тестовый товар',
        supplier_email='неправильный-email',  # Неверный формат
        price=1000.00,
        quantity=5,
        article='GH567890'
    )
    product4.full_clean()
    print("      ✗ Ошибка: валидация должна была провалиться")
except ValidationError as e:
    print(f"      ✓ Валидатор сработал: {e.message_dict.get('supplier_email', [''])[0]}")

# Тест RegexValidator для артикула
print("\n   Тест RegexValidator (неверный формат артикула):")
try:
    product5 = Product(
        name='Тестовый товар',
        supplier_email='test@example.com',
        price=1000.00,
        quantity=5,
        article='неправильный-артикул'  # Неверный формат
    )
    product5.full_clean()
    print("      ✗ Ошибка: валидация должна была провалиться")
except ValidationError as e:
    print(f"      ✓ Валидатор сработал: {e.message_dict.get('article', [''])[0]}")

print("\n" + "=" * 70)
print(f"Всего товаров в БД: {Product.objects.count()}")
print("=" * 70)

