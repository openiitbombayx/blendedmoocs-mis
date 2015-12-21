class IitbxRouter(object):
    """
    A router to control all database operations on models in the
    auth application.
    """
    def db_for_read(self, model, **hints):
        """
        Attempts to read auth models go to iitbxanalysis
        """
        if model._meta.app_label == 'iitbx':
            return 'iitbxanalysis'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth models go to auth_db.
        """
        if model._meta.app_label == 'iitbx':
            return 'iitbxanalysis'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        if obj1._meta.app_label == 'iitbx' or \
           obj2._meta.app_label == 'iitbx':
           return True
        return None

    def allow_migrate(self, db, model):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if db == 'iitbxanalysis':
            return model._meta.app_label == 'iitbx'
        elif model._meta.app_label == 'iitbx':
            return False
        return None
