from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response


class UsersView(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer

    permission_classes = []

    def perform_create(self, serializer):
        # Hash password but passwords are not required
        if ('password' in self.request.data):
            password = make_password(self.request.data['password'])
            serializer.save(password=password)
        else:
            serializer.save()

    def list(self, request, format=None):
        user = Users.objects.get(id_user=self.request.user.id_user)
        dados = {
            "id_user": user.id_user,
            "username": user.username,
            "email": user.email,
            "description": user.description or "",
            "date_birth": user.date_birth,
            "points": user.points or 0,
            "genres": GenresSerializer(user.genres.all(), many=True).data,
            "favorite_books": BooksSerializer(user.favorite_books.all(), many=True).data,
            "reviews": ReviewsSerializer(Review.objects.filter(id_user=user.id_user), many=True).data,
            "bookmarks": TaggedDiscussionsSerializer(TaggedDiscussions.objects.filter(id_user=user.id_user), many=True).data,
            "comments": CommentsSerializer(Comments.objects.filter(id_user=user.id_user), many=True).data,
            "discussions": DiscussionsSerializer(Discussion.objects.filter(id_user=user.id_user), many=True).data
        }

        return Response(dados)
    
    def update(self, request, pk=None, partial=True):
        user = Users.objects.get(id_user=self.request.user.id_user)
        if 'genres' in request.data:
            for genre in request.data['genres']:
                genre = Genre.objects.get(name__iexact=genre)
                user.genres.add(genre)
            
            request.data.pop('genres')
        
        if 'favorite_books' in request.data:
            for book in request.data['favorite_books']:
                book = Book.objects.get(cod_ISBN=book)
                user.favorite_books.add(book)

            request.data.pop('favorite_books')
        serializer = UsersSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class GenresView(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer

class BooksView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer

    permission_classes = []

class ReviewsView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer

class DiscussionsView(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionsSerializer

class TaggedDiscussionsView(viewsets.ModelViewSet):
    queryset = TaggedDiscussions.objects.all()
    serializer_class = TaggedDiscussionsSerializer

class CommentsView(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer