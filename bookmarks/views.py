from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Case, When, Value, F, FloatField


from .models import *
from .serializers import *


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name='title', lookup_expr='icontains')
    author = filters.CharFilter(
        field_name='author', lookup_expr='icontains')
    genres = filters.CharFilter(
        field_name='genres__name', lookup_expr='iexact')

    order_by = filters.OrderingFilter(
        fields=(
            ('published', 'published'),
        )
    )
    class Meta:
        model = Book
        fields = []

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

    @action(detail=False, methods=['get'])
    def leaderboard(self, request):
        current_user = self.request.user

        leaderboard_users = Users.objects.order_by('-points')[:10]

        current_user_position = Users.objects.filter(points__gt=current_user.points or 0).count() + 1

        leaderboard_data = []

        for position, user in enumerate(leaderboard_users, start=1):
            leaderboard_data.append({
                "position": position,
                "username": user.username,
                "points": user.points or 0,
                "isCurrentUser": user == self.request.user
            })

        if current_user not in leaderboard_users:
            current_user_position = Users.objects.filter(points__gt=current_user.points or 0).count() + 1
            if current_user_position > 10:
                leaderboard_data[-1] = {
                    "position": current_user_position,
                    "username": current_user.username,
                    "points": current_user.points or 0,
                    "isCurrentUser": True,
                }
            else:
                leaderboard_data.insert(current_user_position - 1, {
                    "position": current_user_position,
                    "username": current_user.username,
                    "points": current_user.points or 0,
                    "isCurrentUser": True,
                })
                for i in range(current_user_position, len(leaderboard_data)):
                    leaderboard_data[i]['position'] += 1

                leaderboard_data.pop()

        return Response(leaderboard_data)
class GenresView(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenresSerializer

class BooksView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BooksSerializer

    permission_classes = []

    filter_backends = (DjangoFilterBackend,)
    filterset_class = BookFilter
    
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        if 'rating' in request.query_params:
            if request.query_params['rating'] == 'asc':
                queryset = queryset.annotate(
                    custom_rating=Case(
                        When(review__cod_ISBN=F('cod_ISBN'), then=F('review__rating')),
                        default=Value(0),
                        output_field=FloatField()
                    )
                ).order_by('custom_rating')
            elif request.query_params['rating'] == 'desc':
                queryset = queryset.annotate(
                    custom_rating=Case(
                        When(review__cod_ISBN=F('cod_ISBN'), then=F('review__rating')),
                        default=Value(0),
                        output_field=FloatField()
                    )
                ).order_by('-custom_rating')

        serializer = BooksSerializer(queryset, many=True)
        return Response(serializer.data)

class ReviewsView(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewsSerializer

    permission_classes = []

    def perform_create(self, serializer):
        serializer.save(id_user=self.request.user)

class DiscussionsView(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionsSerializer

    permission_classes = []

    def perform_create(self, serializer):
        serializer.save(id_user=self.request.user)

    def list(self, request, format=None):
        discussions = Discussion.objects.all()
        data = []

        for discussion in discussions:
            data.append({
                'id_discussion': discussion.id_discussion,
                'title': discussion.title,
                'description': discussion.description,
                'date': discussion.date,
                'book': {
                    "cod_ISBN": discussion.cod_ISBN.pk,
                    "title": discussion.cod_ISBN.title
                },
                "qty_comments": Comments.objects.filter(id_discussion=discussion.id_discussion).count(),
                "qty_likes": 0,
                "qty_tags": TaggedDiscussions.objects.filter(id_discussion=discussion.id_discussion).count()
            })

        return Response(data)

class TaggedDiscussionsView(viewsets.ModelViewSet):
    queryset = TaggedDiscussions.objects.all()
    serializer_class = TaggedDiscussionsSerializer

class CommentsView(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    def perform_create(self, serializer):
        serializer.save(id_user=self.request.user)