from django.contrib import admin

from .models import UserProfile


# Register your models here.
@admin.register(UserProfile)
class CollaborateRequestAdmin(admin.ModelAdmin):

    list_display = ('user',)