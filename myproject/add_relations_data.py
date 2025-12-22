
import os
import sys
import django
from datetime import date, timedelta

# Настройка Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

from bboard.models import Author, Article, User, UserProfile, Course, Student
from django.core.exceptions import ValidationError

# 1. ONE-TO-MANY (ForeignKey): Author -> Article
print("1. ONE-TO-MANY связь: Author -> Article\n")
# Создание авторов
authors_data = [
    {'name': 'Александр Пушкин', 'email': 'pushkin@example.com', 'bio': 'Великий русский поэт'},
    {'name': 'Лев Толстой', 'email': 'tolstoy@example.com', 'bio': 'Русский писатель, философ'},
    {'name': 'Федор Достоевский', 'email': 'dostoevsky@example.com', 'bio': 'Русский писатель, мыслитель'},
]

authors = []
for author_data in authors_data:
    try:
        # Проверяем существование по email
        author = Author.objects.filter(email=author_data['email']).first()
        if not author:
            author = Author.objects.create(**author_data)
            print(f"   ✓ Создан автор: {author.name}")
        else:
            print(f"   → Автор уже существует: {author.name}")
        authors.append(author)
    except (ValidationError, Exception) as e:
        print(f"   ✗ Ошибка при создании автора {author_data['name']}: {e}")
        authors.append(None)

# Создание статей для авторов (только если авторы созданы)
if len(authors) >= 3 and all(authors[:3]):
    articles_data = [
        {'title': 'Евгений Онегин', 'content': 'Роман в стихах...', 'author': authors[0]},
        {'title': 'Капитанская дочка', 'content': 'Исторический роман...', 'author': authors[0]},
        {'title': 'Война и мир', 'content': 'Эпопея о войне 1812 года...', 'author': authors[1]},
        {'title': 'Анна Каренина', 'content': 'Роман о любви и обществе...', 'author': authors[1]},
        {'title': 'Преступление и наказание', 'content': 'Психологический роман...', 'author': authors[2]},
        {'title': 'Идиот', 'content': 'Роман о князе Мышкине...', 'author': authors[2]},
    ]

    print("\n   Создание статей:")
    for article_data in articles_data:
        try:
            article = Article.objects.filter(title=article_data['title']).first()
            if not article:
                article = Article.objects.create(**article_data)
                print(f"   ✓ Создана статья: '{article.title}' (автор: {article.author.name})")
            else:
                print(f"   → Статья уже существует: '{article.title}'")
        except (ValidationError, Exception) as e:
            print(f"   ✗ Ошибка при создании статьи: {e}")
else:
    print("\n   ⚠ Пропущено создание статей: не все авторы созданы")

# Демонстрация связи
if authors and authors[0]:
    print(f"\n   Демонстрация связи:")
    print(f"   Автор '{authors[0].name}' имеет {authors[0].articles.count()} статей:")
    for article in authors[0].articles.all():
        print(f"      - {article.title}")



# ========== 2. ONE-TO-ONE (OneToOneField): User -> UserProfile ==========
print("2. ONE-TO-ONE связь: User -> UserProfile\n")

# Создание пользователей
users_data = [
    {'username': 'admin', 'email': 'admin@example.com', 'first_name': 'Администратор', 'last_name': 'Системы'},
    {'username': 'manager', 'email': 'manager@example.com', 'first_name': 'Менеджер', 'last_name': 'Отдела'},
    {'username': 'developer', 'email': 'developer@example.com', 'first_name': 'Разработчик', 'last_name': 'Python'},
]

users = []
for user_data in users_data:
    try:
        user = User.objects.filter(email=user_data['email']).first()
        if not user:
            user = User.objects.create(**user_data)
            print(f"   ✓ Создан пользователь: {user.username}")
        else:
            print(f"   → Пользователь уже существует: {user.username}")
        users.append(user)
    except (ValidationError, Exception) as e:
        print(f"   ✗ Ошибка при создании пользователя: {e}")
        users.append(None)

# Создание профилей для пользователей
profiles_data = [
    {'user': users[0], 'phone': '+7 (999) 111-11-11', 'address': 'Москва, ул. Административная, д. 1', 'bio': 'Главный администратор системы'},
    {'user': users[1], 'phone': '+7 (999) 222-22-22', 'address': 'Санкт-Петербург, ул. Менеджерская, д. 2', 'bio': 'Менеджер отдела продаж'},
    {'user': users[2], 'phone': '+7 (999) 333-33-33', 'address': 'Новосибирск, ул. Разработчиков, д. 3', 'bio': 'Python разработчик'},
]

print("\n   Создание профилей:")
for profile_data in profiles_data:
    if not profile_data['user']:
        continue
    try:
        profile = UserProfile.objects.filter(user=profile_data['user']).first()
        if not profile:
            profile = UserProfile.objects.create(**profile_data)
            print(f"   ✓ Создан профиль для пользователя: {profile.user.username}")
        else:
            print(f"   → Профиль уже существует для пользователя: {profile.user.username}")
        print(f"      Телефон: {profile.phone}, Адрес: {profile.address}")
    except (ValidationError, Exception) as e:
        print(f"   ✗ Ошибка при создании профиля: {e}")

# Демонстрация связи
if users and users[0]:
    try:
        print(f"\n   Демонстрация связи:")
        print(f"   Пользователь '{users[0].username}' имеет профиль:")
        print(f"      Имя: {users[0].first_name} {users[0].last_name}")
        print(f"      Email: {users[0].email}")
        if hasattr(users[0], 'profile'):
            print(f"      Телефон профиля: {users[0].profile.phone}")
            print(f"      О себе: {users[0].profile.bio}")
        else:
            print(f"      Профиль не найден")
    except Exception as e:
        print(f"   ⚠ Ошибка при демонстрации связи: {e}")


# ========== 3. MANY-TO-MANY (ManyToManyField): Course <-> Student ==========
print("3. MANY-TO-MANY связь: Course <-> Student\n")

# Создание студентов
students_data = [
    {'name': 'Иван Петров', 'email': 'petrov@student.com', 'phone': '+7 (999) 444-44-44'},
    {'name': 'Мария Сидорова', 'email': 'sidorova@student.com', 'phone': '+7 (999) 555-55-55'},
    {'name': 'Алексей Иванов', 'email': 'ivanov@student.com', 'phone': '+7 (999) 666-66-66'},
    {'name': 'Елена Смирнова', 'email': 'smirnova@student.com', 'phone': '+7 (999) 777-77-77'},
]

students = []
for student_data in students_data:
    try:
        student = Student.objects.filter(email=student_data['email']).first()
        if not student:
            student = Student.objects.create(**student_data)
            print(f"   ✓ Создан студент: {student.name}")
        else:
            print(f"   → Студент уже существует: {student.name}")
        students.append(student)
    except (ValidationError, Exception) as e:
        print(f"   ✗ Ошибка при создании студента: {e}")
        students.append(None)

# Создание курсов
courses_data = [
    {'title': 'Python для начинающих', 'description': 'Основы программирования на Python', 'duration': 40, 'price': 15000.00, 'start_date': date.today() + timedelta(days=7)},
    {'title': 'Django Web Development', 'description': 'Разработка веб-приложений на Django', 'duration': 60, 'price': 25000.00, 'start_date': date.today() + timedelta(days=14)},
    {'title': 'Базы данных SQL', 'description': 'Работа с базами данных и SQL', 'duration': 30, 'price': 12000.00, 'start_date': date.today() + timedelta(days=21)},
]

courses = []
for course_data in courses_data:
    try:
        course = Course.objects.filter(title=course_data['title']).first()
        if not course:
            course = Course.objects.create(**course_data)
            print(f"   ✓ Создан курс: {course.title}")
        else:
            print(f"   → Курс уже существует: {course.title}")
        courses.append(course)
    except (ValidationError, Exception) as e:
        print(f"   ✗ Ошибка при создании курса: {e}")
        courses.append(None)

# Добавление студентов на курсы (многие ко многим)
if len(courses) >= 3 and len(students) >= 4 and all(courses[:3]) and all(students[:4]):
    print("\n   Добавление студентов на курсы:")
    # Курс 1: Python для начинающих
    if courses[0] and students[0] and students[1] and students[2]:
        # Добавляем только тех, кого еще нет
        existing = set(courses[0].students.all())
        to_add = [s for s in [students[0], students[1], students[2]] if s not in existing]
        if to_add:
            courses[0].students.add(*to_add)
        print(f"   ✓ На курс '{courses[0].title}' записано {courses[0].students.count()} студентов")

    # Курс 2: Django Web Development
    if courses[1] and students[1] and students[2] and students[3]:
        existing = set(courses[1].students.all())
        to_add = [s for s in [students[1], students[2], students[3]] if s not in existing]
        if to_add:
            courses[1].students.add(*to_add)
        print(f"   ✓ На курс '{courses[1].title}' записано {courses[1].students.count()} студентов")

    # Курс 3: Базы данных SQL
    if courses[2] and students[0] and students[3]:
        existing = set(courses[2].students.all())
        to_add = [s for s in [students[0], students[3]] if s not in existing]
        if to_add:
            courses[2].students.add(*to_add)
        print(f"   ✓ На курс '{courses[2].title}' записано {courses[2].students.count()} студентов")

    # Демонстрация связи
    if students[1]:
        print(f"\n   Демонстрация связи:")
        print(f"   Студент '{students[1].name}' посещает {students[1].courses.count()} курса:")
        for course in students[1].courses.all():
            print(f"      - {course.title} (цена: {course.price} руб.)")

    if courses[0]:
        print(f"\n   Курс '{courses[0].title}' посещают {courses[0].students.count()} студентов:")
        for student in courses[0].students.all():
            print(f"      - {student.name} ({student.email})")
else:
    print("\n   ⚠ Пропущено добавление студентов на курсы: не все данные созданы")

print("ИТОГОВАЯ СТАТИСТИКА:")

print(f"Авторов: {Author.objects.count()}")
print(f"Статей: {Article.objects.count()}")
print(f"Пользователей: {User.objects.count()}")
print(f"Профилей: {UserProfile.objects.count()}")
print(f"Студентов: {Student.objects.count()}")
print(f"Курсов: {Course.objects.count()}")

