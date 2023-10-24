from django.contrib.auth.hashers import make_password
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Case, When, Value, F, FloatField, Count

from .models import *
from .serializers import *


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(
        field_name='title', lookup_expr='icontains')
    author = filters.CharFilter(
        field_name='author', lookup_expr='iexact')

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
        discussions = Discussion.objects.filter(id_user=user.id_user)
        
        discussions_data = []

        for discussion in discussions:
            discussions_data.append({
                'id_discussion': discussion.id_discussion,
                'title': discussion.title,
                'description': discussion.description,
                'date': discussion.date,
                "cod_ISBN": discussion.cod_ISBN.pk,
                "qty_comments": discussion.qty_comments,
                "qty_likes": discussion.qty_likes,
                "qty_tags": discussion.qty_tags,
                "is_tagged": TaggedDiscussions.objects.filter(id_discussion=discussion.id_discussion, id_user=self.request.user).exists(),
                "is_liked": LikedDiscussions.objects.filter(id_discussion=discussion.id_discussion, id_user=self.request.user).exists(),
                "is_author": discussion.id_user == self.request.user,
                'is_adult': discussion.is_adult,
                'is_spoiler': discussion.is_spoiler,
                "author": discussion.id_user.username,
            })

        bookmarks = TaggedDiscussions.objects.filter(id_user=user.id_user)

        bookmarks_data = []

        for bookmark in bookmarks:
            bookmarks_data.append({
                'id_discussion': bookmark.id_discussion.id_discussion,
                'title': bookmark.id_discussion.title,
                'description': bookmark.id_discussion.description,
                'date': bookmark.id_discussion.date,
                "cod_ISBN": bookmark.id_discussion.cod_ISBN.pk,
                "qty_comments": bookmark.id_discussion.qty_comments,
                "qty_likes": bookmark.id_discussion.qty_likes,
                "qty_tags": bookmark.id_discussion.qty_tags,
                "is_tagged": TaggedDiscussions.objects.filter(id_discussion=bookmark.id_discussion.id_discussion, id_user=self.request.user).exists(),
                "is_liked": LikedDiscussions.objects.filter(id_discussion=bookmark.id_discussion.id_discussion, id_user=self.request.user).exists(),
                "is_author": bookmark.id_discussion.id_user == self.request.user,
                'is_adult': bookmark.id_discussion.is_adult,
                'is_spoiler': bookmark.id_discussion.is_spoiler,
                "author": bookmark.id_discussion.id_user.username,
            })
        
        comments = Comments.objects.filter(id_user=user.id_user)

        comments_data = []

        for comment in comments:
            comments_data.append({
                'id_comment': comment.id_comment,
                'description': comment.description,
                'date': comment.date,
                "id_discussion": comment.id_discussion.pk,
                "author": comment.id_user.username,
                "is_liked": LikedComments.objects.filter(id_comment=comment.id_comment, id_user=self.request.user).exists(),
                "book": comment.id_discussion.cod_ISBN.pk
            })

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
            "bookmarks": bookmarks_data,
            "comments": comments_data,
            "discussions": discussions_data
        }

        return Response(dados)
    
    def update(self, request, pk=None, partial=True):
        user = Users.objects.get(id_user=self.request.user.id_user)
        if 'genres' in request.data:
            user.genres.clear()
            for genre in request.data['genres']:
                genre = Genre.objects.get(name__iexact=genre)
                user.genres.add(genre)
            
            request.data.pop('genres')
        
        if 'favorite_book' in request.data:
            book = Book.objects.get(cod_ISBN=request.data['favorite_book'])
            if book not in user.favorite_books.all():
                user.favorite_books.add(book)
            else:
                user.favorite_books.remove(book)

            request.data.pop('favorite_book')
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
    
    @action(detail=True, methods=['get'])
    def user(self, request, pk=None):
        user = Users.objects.get(username__iexact=pk)
        discussions = Discussion.objects.filter(id_user=user.id_user)
        
        discussions_data = []

        for discussion in discussions:
            discussions_data.append({
                'id_discussion': discussion.id_discussion,
                'title': discussion.title,
                'description': discussion.description,
                'date': discussion.date,
                "cod_ISBN": discussion.cod_ISBN.pk,
                "qty_comments": discussion.qty_comments,
                "qty_likes": discussion.qty_likes,
                "qty_tags": discussion.qty_tags,
                "is_tagged": TaggedDiscussions.objects.filter(id_discussion=discussion.id_discussion, id_user=self.request.user).exists(),
                "is_liked": LikedDiscussions.objects.filter(id_discussion=discussion.id_discussion, id_user=self.request.user).exists(),
                "is_author": discussion.id_user == self.request.user,
                'is_adult': discussion.is_adult,
                'is_spoiler': discussion.is_spoiler,
            })

        bookmarks = TaggedDiscussions.objects.filter(id_user=user.id_user)

        bookmarks_data = []

        for bookmark in bookmarks:
            bookmarks_data.append({
                'id_discussion': bookmark.id_discussion.id_discussion,
                'title': bookmark.id_discussion.title,
                'description': bookmark.id_discussion.description,
                'date': bookmark.id_discussion.date,
                "cod_ISBN": bookmark.id_discussion.cod_ISBN.pk,
                "qty_comments": bookmark.id_discussion.qty_comments,
                "qty_likes": bookmark.id_discussion.qty_likes,
                "qty_tags": bookmark.id_discussion.qty_tags,
                "is_tagged": TaggedDiscussions.objects.filter(id_discussion=bookmark.id_discussion.id_discussion, id_user=self.request.user).exists(),
                "is_liked": LikedDiscussions.objects.filter(id_discussion=bookmark.id_discussion.id_discussion, id_user=self.request.user).exists(),
                "is_author": bookmark.id_discussion.id_user == self.request.user,
                'is_adult': bookmark.id_discussion.is_adult,
                'is_spoiler': bookmark.id_discussion.is_spoiler,
                "author": bookmark.id_discussion.id_user.username,
            })
        
        comments = Comments.objects.filter(id_user=user.id_user)

        comments_data = []

        for comment in comments:
            comments_data.append({
                'id_comment': comment.id_comment,
                'description': comment.description,
                'date': comment.date,
                "id_discussion": comment.id_discussion.pk,
                "author": comment.id_user.username,
                "is_liked": LikedComments.objects.filter(id_comment=comment.id_comment, id_user=self.request.user).exists(),
                'likes': LikedComments.objects.filter(id_comment=comment.id_comment).count(),
                'answers': Comments.objects.filter(id_related_comment=comment.id_comment).count(),
                "book": comment.id_discussion.cod_ISBN.pk
            })

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
            "bookmarks": bookmarks_data,
            "comments": comments_data,
            "discussions": discussions_data
        }

        return Response(dados)

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

        if 'popularity' in request.query_params:
            if request.query_params['popularity'] == 'asc':
                queryset = queryset.annotate(
                    custom_popularity=Count('review')
                ).order_by('custom_popularity')
            elif request.query_params['popularity'] == 'desc':
                queryset = queryset.annotate(
                    custom_popularity=Count('review')
                ).order_by('-custom_popularity')

        serializer = BooksSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action (detail=True, methods=['get'])
    def reviews(self, request, pk=None):
        book = Book.objects.get(cod_ISBN=pk)
        reviews = Review.objects.filter(cod_ISBN=book.cod_ISBN)

        data = []

        for review in reviews:
            data.append({
                'id_review': review.id_review,
                'title': review.title,
                'description': review.description,
                'rating': review.rating,
                'date': review.date,
                'is_adult': review.is_adult,
                'is_spoiler': review.is_spoiler,
                'book': {
                    "cod_ISBN": review.cod_ISBN.pk,
                    "title": review.cod_ISBN.title
                },
                'author': review.id_user.username
            })

        return Response(data)
    
    @action (detail=True, methods=['get'])
    def discussions(self, request, pk=None):
        current_user = self.request.user
        book = Book.objects.get(cod_ISBN=pk)
        discussions = Discussion.objects.filter(cod_ISBN=book.cod_ISBN)

        data = []

        for discussion in discussions:
            data.append({
                'id_discussion': discussion.id_discussion,
                'title': discussion.title,
                'description': discussion.description,
                'date': discussion.date,
                'is_adult': discussion.is_adult,
                'is_spoiler': discussion.is_spoiler,
                'book': {
                    "cod_ISBN": discussion.cod_ISBN.pk,
                    "title": discussion.cod_ISBN.title
                },
                "qty_comments": discussion.qty_comments,
                "qty_likes": discussion.qty_likes,
                "qty_tags": discussion.qty_tags,
                "author": discussion.id_user.username,
                "is_tagged": TaggedDiscussions.objects.filter(id_discussion=discussion.id_discussion, id_user=self.request.user).exists(),
                "is_liked": LikedDiscussions.objects.filter(id_discussion=discussion.id_discussion, id_user=self.request.user).exists(),
                "is_author": discussion.id_user == current_user,
            })

        return Response(data)

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
        current_user = self.request.user
        print(current_user)
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
                "qty_comments": discussion.qty_comments,
                "qty_likes": discussion.qty_likes,
                "qty_tags": discussion.qty_tags,
                "is_tagged": TaggedDiscussions.objects.filter(id_discussion=discussion.id_discussion, id_user=current_user).exists(),
                "is_liked": LikedDiscussions.objects.filter(id_discussion=discussion.id_discussion, id_user=current_user).exists(),
                "is_author": discussion.id_user == current_user,
                "author": discussion.id_user.username,
            })

        return Response(data)
    
    def retrieve(self, request, pk=None):
        current_user = self.request.user
        try:
            discussion = Discussion.objects.get(id_discussion=pk)
        except Discussion.DoesNotExist:
            return Response({"error": "Discussion not found"}, status=404)
        
        comments = []

        for comment in Comments.objects.filter(id_discussion=discussion.id_discussion):
            if comment.is_root:
                comments.append({
                    'id_comment': comment.id_comment,
                    'description': comment.description,
                    'date': comment.date,
                    "id_discussion": comment.id_discussion.pk,
                    "author": comment.author,
                    "is_liked": LikedComments.objects.filter(id_comment=comment.id_comment, id_user=current_user).exists(),
                    'likes': comment.likes,
                    'qty_answers': comment.answers.count(),
                    'depth': comment.depth
                })

        data = {
            'id_discussion': discussion.id_discussion,
            'title': discussion.title,
            'description': discussion.description,
            'date': discussion.date,
            "cod_ISBN": discussion.cod_ISBN.pk,
            "qty_comments": discussion.qty_comments,
            "qty_likes": discussion.qty_likes,
            "qty_tags": discussion.qty_tags,
            "is_tagged": TaggedDiscussions.objects.filter(id_discussion=discussion.id_discussion, id_user=current_user).exists(),
            "is_liked": LikedDiscussions.objects.filter(id_discussion=discussion.id_discussion, id_user=current_user).exists(),
            "is_author": discussion.id_user == current_user,
            "is_adult": discussion.is_adult,
            "is_spoiler": discussion.is_spoiler,
            "author": discussion.id_user.username,
            "comments": comments
        }

        return Response(data)

    @action(detail=True, methods=['get'])
    def like(self, request, pk=None):
        current_user = self.request.user

        discussion = Discussion.objects.get(id_discussion=pk)
        user = Users.objects.get(id_user=current_user.id_user)

        liked, created = LikedDiscussions.objects.get_or_create(id_user=user, id_discussion=discussion)

        if not created:
            liked.delete()
            return Response({"is_liked": False})
        else:
            return Response({"is_liked": True})
        

    @action(detail=True, methods=['get'])
    def bookmark(self, request, pk=None):
        current_user = self.request.user
        discussion = Discussion.objects.get(id_discussion=pk)
        user = Users.objects.get(id_user=current_user.id_user)

        tagged, created = TaggedDiscussions.objects.get_or_create(id_user=user, id_discussion=discussion)

        if not created:
            tagged.delete()
            return Response({"is_tagged": False})
        else:
            return Response({"is_tagged": True})

class TaggedDiscussionsView(viewsets.ModelViewSet):
    queryset = TaggedDiscussions.objects.all()
    serializer_class = TaggedDiscussionsSerializer

class CommentsView(viewsets.ModelViewSet):
    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer

    permission_classes = []

    def perform_create(self, serializer):
        serializer.save(id_user=self.request.user)

    @action(detail=True, methods=['get'])
    def like(self, request, pk=None):
        current_user = self.request.user

        comment = Comments.objects.get(id_comment=pk)
        user = Users.objects.get(id_user=current_user.id_user)

        liked, created = LikedComments.objects.get_or_create(id_user=user, id_comment=comment)

        if not created:
            liked.delete()
            return Response({"is_liked": False})
        else:
            return Response({"is_liked": True})
        
    @action(detail=True, methods=['get'])
    def answers(self, request, pk=None):
        comment = Comments.objects.get(id_comment=pk)
        answers = Comments.objects.filter(id_related_comment=comment.id_comment)

        data = []

        for answer in answers:
            data.append({
                'id_comment': answer.id_comment,
                'description': answer.description,
                'date': answer.date,
                "id_discussion": answer.id_discussion.pk,
                "author": answer.id_user.username,
                "is_liked": LikedComments.objects.filter(id_comment=answer.id_comment, id_user=self.request.user).exists(),
                'likes': LikedComments.objects.filter(id_comment=answer.id_comment).count(),
                'qty_answers': Comments.objects.filter(id_related_comment=answer.id_comment).count(),
                'depth': answer.depth
            })

        return Response(data)