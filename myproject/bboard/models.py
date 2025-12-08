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