
class DatabaseRouter:
    """
    Router для определения, какая модель в какую БД должна идти
    """
    # Модели, которые должны использовать utility БД (MySQL на Jino.ru)
    utility_models = {'SiteLog'}
    
    def db_for_read(self, model, **hints):
        """Указывает, какую БД использовать для чтения"""
        if model._meta.label.split('.')[-1] in self.utility_models:
            return 'utility'
        return 'default'
    
    def db_for_write(self, model, **hints):
        """Указывает, какую БД использовать для записи"""
        if model._meta.label.split('.')[-1] in self.utility_models:
            return 'utility'
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """Разрешает связи между объектами из разных БД"""
        db_set = {'default', 'utility'}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return True
        return None
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """Указывает, можно ли применять миграции к БД"""
        if model_name in self.utility_models:
            return db == 'utility'
        elif db == 'utility':
            return False
        return db == 'default'

