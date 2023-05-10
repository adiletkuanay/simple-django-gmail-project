from django.contrib import admin
from .models import Message
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

# Register your models here.
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',)
    search_fields = ('subject',)
admin.site.register(Message, MessageAdmin)