class DevsRouter:
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Only put models from 'app1' into the 'users_db' database
        if app_label == 'devs':
            return db == 'default'
        # All other models go to 'default'
        return db == 'default'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'devs':
            return 'default'   # Read from analytics database
        return 'default'  

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'devs':
            return 'default'  # All user writes go here
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations only if both objects are in the same DB
        if obj1._state.db == obj2._state.db:
            return True
        return False
