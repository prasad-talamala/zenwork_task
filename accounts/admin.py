from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'city', 'state', 'pin_code')
    list_display_links = ('id', 'user')
    list_per_page = 25


admin.site.register(UserProfile, UserProfileAdmin)
