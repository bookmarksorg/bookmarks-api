from rest_framework import routers
from .views import *

routerBookmarks = routers.DefaultRouter()
routerBookmarks.register(r'users', UsersView)
routerBookmarks.register(r'genres', GenresView)
routerBookmarks.register(r'books', BooksView)
routerBookmarks.register(r'reviews', ReviewsView)
routerBookmarks.register(r'discussions', DiscussionsView)
routerBookmarks.register(r'taggeddiscussions', TaggedDiscussionsView)
routerBookmarks.register(r'comments', CommentsView)