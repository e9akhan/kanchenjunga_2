"""
    Module name :- apps
"""


from django.apps import AppConfig


class StoreConfig(AppConfig):
    """
        App config.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'store'
