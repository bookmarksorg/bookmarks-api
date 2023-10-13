from django.contrib import admin
from .models import *

# Register your models here.
class UsersForm(admin.ModelAdmin): 
    list_display = ['username', 'email', 'date_birth', 'points']
    list_filter = ['genres']

class BooksForm(admin.ModelAdmin):
    list_display = ['title', 'number_pages']


admin.site.register(Users, UsersForm)
admin.site.register(Book, BooksForm)