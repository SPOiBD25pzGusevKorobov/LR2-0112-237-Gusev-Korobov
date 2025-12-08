from django.db import models

class Bb(models.Model):
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    published = models.DateTimeField(auto_now_add=True, db_index=True,
verbose_name='Опубликовано')
    rubric = models.ForeignKey('Rubric', null=True,
                               on_delete=models.PROTECT, verbose_name='Рубрика')
class Meta:
    verbose_name_plural = 'Объявления'
    verbose_name = 'Объявление'
    ordering = ['-published']

class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True,
                                        verbose_name='Название')
    def __str__(self):
        return self.name
class Meta:
    verbose_name_plural = 'Рубрики'
    verbose_name = 'Рубрика'
    ordering = ['name']

# Модель для базы данных на Jino.ru (utility)
class SiteLog(models.Model):
    action = models.CharField(max_length=100, verbose_name='Действие')
    description = models.TextField(verbose_name='Описание')
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name='IP адрес')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')
    
    class Meta:
        verbose_name_plural = 'Логи сайта'
        verbose_name = 'Лог сайта'
        ordering = ['-created_at']
        db_table = 'site_logs'
    
    def __str__(self):
        return f"{self.action} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"

# Модели со связью один ко многим
class Author(models.Model):
    """Модель Автор - один автор может иметь много статей"""
    name = models.CharField(max_length=100, verbose_name='Имя автора')
    email = models.EmailField(verbose_name='Email')
    bio = models.TextField(blank=True, verbose_name='Биография')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    
    class Meta:
        verbose_name_plural = 'Авторы'
        verbose_name = 'Автор'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Article(models.Model):
    """Модель Статья - многие статьи принадлежат одному автору"""
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержание')
    author = models.ForeignKey(
        Author, 
        on_delete=models.CASCADE, 
        related_name='articles',
        verbose_name='Автор'
    )
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Опубликовано')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    
    class Meta:
        verbose_name_plural = 'Статьи'
        verbose_name = 'Статья'
        ordering = ['-published']
    
    def __str__(self):
        return self.title

# Модели со связью один к одному (OneToOne)
class User(models.Model):
    """Модель Пользователь - один пользователь имеет один профиль"""
    username = models.CharField(max_length=50, unique=True, verbose_name='Имя пользователя')
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=50, verbose_name='Имя')
    last_name = models.CharField(max_length=50, verbose_name='Фамилия')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    
    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
        ordering = ['username']
    
    def __str__(self):
        return self.username

class UserProfile(models.Model):
    """Модель Профиль пользователя - один профиль принадлежит одному пользователю"""
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name='Пользователь'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    address = models.TextField(blank=True, verbose_name='Адрес')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    avatar_url = models.URLField(blank=True, verbose_name='URL аватара')
    bio = models.TextField(blank=True, verbose_name='О себе')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    class Meta:
        verbose_name_plural = 'Профили пользователей'
        verbose_name = 'Профиль пользователя'
    
    def __str__(self):
        return f"Профиль {self.user.username}"

# Модели со связью многие ко многим (Many-to-Many)
class Course(models.Model):
    """Модель Курс - один курс может иметь много студентов, один студент может посещать много курсов"""
    title = models.CharField(max_length=200, verbose_name='Название курса')
    description = models.TextField(verbose_name='Описание')
    duration = models.IntegerField(verbose_name='Длительность (часов)')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    start_date = models.DateField(verbose_name='Дата начала')
    students = models.ManyToManyField(
        'Student',
        related_name='courses',
        blank=True,
        verbose_name='Студенты'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name_plural = 'Курсы'
        verbose_name = 'Курс'
        ordering = ['title']
    
    def __str__(self):
        return self.title

class Student(models.Model):
    """Модель Студент - один студент может посещать много курсов, один курс может иметь много студентов"""
    name = models.CharField(max_length=100, verbose_name='Имя студента')
    email = models.EmailField(unique=True, verbose_name='Email')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    enrollment_date = models.DateField(auto_now_add=True, verbose_name='Дата зачисления')
    
    class Meta:
        verbose_name_plural = 'Студенты'
        verbose_name = 'Студент'
        ordering = ['name']
    
    def __str__(self):
        return self.name