from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import User, Subscription


@admin.register(User)
class CustomUser(UserAdmin):
    list_filter = ('email', 'username')


admin.site.register(Subscription)