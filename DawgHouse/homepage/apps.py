"""
Configures apps
"""

from django.apps import AppConfig

class HomepageConfig(AppConfig):
    """Configures homepage app"""
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homepage'
