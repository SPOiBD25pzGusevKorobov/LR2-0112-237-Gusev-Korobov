from django.db import models
from django.core.validators import (
    MinValueValidator, MaxValueValidator,
    MinLengthValidator, MaxLengthValidator,
    EmailValidator, URLValidator,
    RegexValidator, DecimalValidator
)
from PIL import Image
import os

class Bb(models.Model):
    """Модель объявления"""
    title = models.CharField(max_length=50, verbose_name='Товар')
    content = models.TextField(verbose_name='Описание')
    price = models.FloatField(verbose_name='Цена')
    published = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Опубликовано'
    )
    rubric = models.ForeignKey(
        'Rubric',
        null=True,
        on_delete=models.PROTECT,
        verbose_name='Рубрика'
    )

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published']


class Rubric(models.Model):
    """Модель рубрики"""
    name = models.CharField(
        max_length=20,
        db_index=True,
        verbose_name='Название'
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['name']

class SiteLog(models.Model):
    """Модель для базы данных на Jino.ru (utility)"""
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


class Author(models.Model):
    """Модель Автор - один автор может иметь много статей"""
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


class User(models.Model):
    """Модель Пользователь - один пользователь имеет один профиль"""
    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Имя пользователя'
    )
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


class Course(models.Model):
    """Модель Курс - один курс может иметь много студентов, один студент может посещать много курсов"""
    title = models.CharField(
        max_length=200,
        verbose_name='Название курса'
    )
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


class Product(models.Model):
    """Модель Товар с различными валидаторами Django"""
    name = models.CharField(
        max_length=100,
        verbose_name='Название товара',
        validators=[
            MinLengthValidator(3, message='Название должно содержать минимум 3 символа'),
            MaxLengthValidator(100, message='Название не должно превышать 100 символов'),
        ]
    )
    supplier_email = models.EmailField(
        verbose_name='Email поставщика',
        validators=[EmailValidator(message='Введите корректный email адрес')]
    )
    product_url = models.URLField(
        blank=True,
        verbose_name='Ссылка на товар',
        validators=[URLValidator(message='Введите корректный URL')]
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена',
        validators=[
            MinValueValidator(0.01, message='Цена должна быть больше 0'),
            MaxValueValidator(9999999.99, message='Цена не должна превышать 9999999.99'),
        ]
    )
    quantity = models.IntegerField(
        verbose_name='Количество',
        validators=[
            MinValueValidator(0, message='Количество не может быть отрицательным'),
            MaxValueValidator(10000, message='Количество не должно превышать 10000'),
        ]
    )
    phone_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message='Телефон должен быть в формате: +79991234567'
    )
    supplier_phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='Телефон поставщика',
        validators=[phone_validator]
    )
    article_validator = RegexValidator(
        regex=r'^[A-Z]{2}\d{6}$',
        message='Артикул должен быть в формате: AB123456 (2 буквы + 6 цифр)'
    )
    article = models.CharField(
        max_length=10,
        unique=True,
        verbose_name='Артикул',
        validators=[article_validator]
    )
    discount_percent = models.IntegerField(
        default=0,
        verbose_name='Процент скидки',
        validators=[
            MinValueValidator(0, message='Скидка не может быть отрицательной'),
            MaxValueValidator(100, message='Скидка не может превышать 100%'),
        ]
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name_plural = 'Товары'
        verbose_name = 'Товар'
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Recipe(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название рецепта')
    description = models.TextField(verbose_name='Описание рецепта', blank=True)
    image = models.ImageField(
        upload_to='recipes/',
        blank=True,
        null=True,
        verbose_name='Изображение рецепта'
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    
    class Meta:
        verbose_name_plural = 'Рецепты'
        verbose_name = 'Рецепт'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """Переопределяем save для автоматического изменения размера изображения"""
        # Сохраняем сначала, чтобы получить путь к изображению
        super().save(*args, **kwargs)
        
        if self.image and os.path.exists(self.image.path):
            try:
                # Открываем изображение
                img = Image.open(self.image.path)
                
                # Конвертируем в RGB, если нужно (для JPEG)
                if img.mode in ('RGBA', 'LA', 'P'):
                    rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = rgb_img
                
                # Максимальные размеры для изображения
                max_width = 800
                max_height = 600
                
                # Проверяем, нужно ли изменять размер
                if img.width > max_width or img.height > max_height:
                    # Вычисляем новые размеры с сохранением пропорций
                    img.thumbnail((max_width, max_height), Image.Resampling.LANCZOS)
                    
                    # Сохраняем измененное изображение с оптимизацией
                    img.save(self.image.path, optimize=True, quality=85)
            except Exception:
                # Если произошла ошибка при обработке изображения, просто пропускаем
                # Это не должно блокировать сохранение рецепта
                pass


class Ingredient(models.Model):
    """Модель Ингредиент - многие ингредиенты принадлежат одному рецепту"""
    UNIT_CHOICES = [
        ('г', 'граммы'),
        ('кг', 'килограммы'),
        ('мл', 'миллилитры'),
        ('л', 'литры'),
        ('шт', 'штуки'),
        ('ст.л.', 'столовые ложки'),
        ('ч.л.', 'чайные ложки'),
        ('стакан', 'стаканы'),
        ('щепотка', 'щепотки'),
    ]
    
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredients',
        verbose_name='Рецепт'
    )
    name = models.CharField(max_length=200, verbose_name='Название ингредиента')
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Количество',
        validators=[MinValueValidator(0.01, message='Количество должно быть больше 0')]
    )
    unit = models.CharField(
        max_length=20,
        choices=UNIT_CHOICES,
        default='г',
        verbose_name='Единица измерения'
    )
    order = models.IntegerField(default=0, verbose_name='Порядок сортировки')
    
    class Meta:
        verbose_name_plural = 'Ингредиенты'
        verbose_name = 'Ингредиент'
        ordering = ['order', 'name']
    
    def __str__(self):
        return f"{self.name} - {self.quantity} {self.get_unit_display()}"