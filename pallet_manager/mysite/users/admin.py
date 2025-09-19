# pallet_manager/mysite/users/admin.py
from django.contrib import admin
from django.contrib.auth import get_user_model

CustomUser = get_user_model()
admin.site.register(CustomUser)