from rest_framework import serializers
from .models import *

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genres
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = fields = '__all__'
    
class BooksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = '__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = '__all__'

class DiscussionsSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Discussions
        fields = '__all__'

    def to_representation(self, obj):
        qty_comments = 0
        qty_likes = 0
        qty_tags = 0
        

        book = {
            "cod_ISBN": obj.cod_ISBN.pk,
            "title": obj.cod_ISBN.title
        },
        return {
            'id_discussion': obj.id_discussion,
            'title': obj.title,
            'description': obj.description,
            'date': obj.date,
            'book': book,
            "qty_comments": qty_comments,
            "qty_likes": qty_likes,
            "qty_tags": qty_tags
        },

class TaggedDiscussionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaggedDiscussions
        fields = '__all__'

    def to_representation(self, obj):
        qty_comments = 0
        qty_likes = 0
        qty_tags = 0

        book = {
            "cod_ISBN": obj.id_discussion.cod_ISBN.pk,
            "title": obj.id_discussion.cod_ISBN.title
        },
        discussions = {
            'id_discussion': obj.id_discussion.pk,
            'title': obj.id_discussion.title,
            'description': obj.id_discussion.description,
            'date': obj.id_discussion.date,
            'book': book,
            "qty_comments": qty_comments,
            "qty_likes": qty_likes,
            "qty_tags": qty_tags
        },
        return {
            'id_user': obj.id_user.pk,
            'username': obj.id_user.username,
            "discussions": discussions,
        }

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'