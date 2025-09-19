# polls/admin.py  (o la app que tengas en INSTALLED_APPS)
from django.contrib import admin
from django.contrib.auth.models import User

admin.site.register(User)
