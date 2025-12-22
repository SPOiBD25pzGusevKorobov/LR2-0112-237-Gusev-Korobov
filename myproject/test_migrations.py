
"""
Скрипт для демонстрации работы с миграциями:
- Просмотр миграций
- Отмена миграций (rollback)
- Применение миграций
Запуск: python test_migrations.py (из папки myproject)
"""
import os
import sys
import django
import subprocess

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from django.core.management import call_command
from io import StringIO

print("ДЕМОНСТРАЦИЯ РАБОТЫ С МИГРАЦИЯМИ")

# 1. Просмотр текущих миграций
print("1. Текущее состояние миграций bboard:")
out = StringIO()
call_command('showmigrations', 'bboard', stdout=out)
migrations_output = out.getvalue()
print(migrations_output)

# Подсчет примененных миграций
applied = migrations_output.count('[X]')
unapplied = migrations_output.count('[ ]')
print(f"\n   Применено миграций: {applied}")
print(f"   Не применено миграций: {unapplied}")


# 2. Демонстрация отмены миграции (rollback)
print("2. ДЕМОНСТРАЦИЯ ОТМЕНЫ МИГРАЦИЙ (ROLLBACK):")


# Откат последней миграции (если есть примененные)
if applied > 0:
    print("\n   Откат миграции 0012_migration_3_add_views (удаление поля views_count):")
    try:
        call_command('migrate', 'bboard', '0011_migration_2_add_featured', verbosity=1)
        print("   ✓ Миграция успешно отменена")
    except Exception as e:
        print(f"   ✗ Ошибка при откате: {e}")
    
    print("\n   Состояние после отката:")
    out = StringIO()
    call_command('showmigrations', 'bboard', stdout=out)
    print(out.getvalue())
    
    # Применение миграции обратно
    print("\n   Применение миграции обратно:")
    try:
        call_command('migrate', 'bboard', verbosity=1)
        print("   ✓ Миграция успешно применена")
    except Exception as e:
        print(f"   ✗ Ошибка при применении: {e}")
else:
    print("   Нет примененных миграций для отката")


# 3. Информация о слиянии миграций
print("3. ИНФОРМАЦИЯ О СЛИЯНИИ МИГРАЦИЙ:")
print("   Создано слияние миграций:")
print("   - 0010_migration_1_add_rating_squashed_0012_migration_3_add_views")
print("   (объединяет миграции 0010, 0011, 0012)")
print("\n   Для применения слияния выполните:")
print("   python manage.py migrate bboard")

print("ДЕМОНСТРАЦИЯ ЗАВЕРШЕНА")


