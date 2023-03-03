from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import Subscription, User


@admin.register(User)
class CustomUser(UserAdmin):
    list_filter = ('email', 'username')


admin.site.register(Subscription)
