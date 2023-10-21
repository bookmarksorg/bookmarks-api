from django.contrib import admin
from .models import *

# Register your models here.
class UsersForm(admin.ModelAdmin): 
    list_display = ['username', 'email', 'date_birth', 'points']
    list_filter = ['genres']

class BooksForm(admin.ModelAdmin):
    list_display = ['title', 'number_pages']

class ReviewsForm(admin.ModelAdmin):
    list_display = ['title', 'id_user']

class DiscussionsForm(admin.ModelAdmin):
    list_display = ['title', 'id_user']

class GenresForm(admin.ModelAdmin):
    list_display = ['name']

class CommentsForm(admin.ModelAdmin):
    list_display = ['id_user', 'id_discussion']


admin.site.register(Comments, CommentsForm)
admin.site.register(Genre, GenresForm)
admin.site.register(Users, UsersForm)
admin.site.register(Book, BooksForm)
admin.site.register(Review, ReviewsForm)
admin.site.register(Discussion, DiscussionsForm)