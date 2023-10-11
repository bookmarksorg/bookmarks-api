from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.views import APIView


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
        pk = Users.objects.get(id_user=self.request.user.id_user).id_user

        dados = {
            "user": UsersSerializer(Users.objects.get(id_user=int(pk))).data,
            "tagged": TaggedDiscussionsSerializer(TaggedDiscussions.objects.filter(id_user=int(pk)),many=True).data,
            "comments": CommentsSerializer(Comments.objects.filter(id_user=int(pk)), many=True).data,
            "discussions": DiscussionsSerializer(Discussions.objects.filter(id_user=int(pk)), many=True).data
        }

        return Response(dados)

class GenresView(viewsets.ModelViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer

class BooksView(viewsets.ModelViewSet):
    queryset = Books.objects.all()
    serializer_class = BooksSerializer

class ReviewsView(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer

class DiscussionsView(viewsets.ModelViewSet):
    queryset = Discussions.objects.all()
    serializer_class = DiscussionsSerializer

class TaggedDiscussionsView(viewsets.ModelViewSet):
    queryset = TaggedDiscussions.objects.all()
    serializer_class = TaggedDiscussionsSerializer

class CommentsView(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer