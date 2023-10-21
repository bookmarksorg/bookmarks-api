from rest_framework import serializers
from .models import *

class GenresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = '__all__'
    
class BooksSerializer(serializers.ModelSerializer):
    qty_reviews = serializers.ReadOnlyField()
    qty_discussions = serializers.ReadOnlyField()
    rating = serializers.ReadOnlyField()

    class Meta:
        model = Book
        fields = '__all__'

class ReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class DiscussionsSerializer(serializers.ModelSerializer):
    qty_likes = serializers.ReadOnlyField()
    qty_comments = serializers.ReadOnlyField()
    qty_tags = serializers.ReadOnlyField()

    class Meta:
        model = Discussion
        fields = '__all__'

class TaggedDiscussionsSerializer(serializers.ModelSerializer):
    qty_likes = serializers.ReadOnlyField()
    qty_comments = serializers.ReadOnlyField()
    qty_tags = serializers.ReadOnlyField()
    author = serializers.ReadOnlyField(source='id_user.username')

    class Meta:
        model = TaggedDiscussions
        fields = '__all__'

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = '__all__'