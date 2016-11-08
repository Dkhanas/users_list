from django.contrib import admin

# Register your models here.
from user_app_list.models import User, Comments

admin.site.register(User)
admin.site.register(Comments)
