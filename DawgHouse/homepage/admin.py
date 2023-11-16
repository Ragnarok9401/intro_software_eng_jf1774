"""
Registers models in admin portal
"""

from django.contrib import admin
from .models import DawgHouseUser, Bark, Comment

# Register your models here.
admin.site.register(DawgHouseUser)
admin.site.register(Bark)
admin.site.register(Comment)
