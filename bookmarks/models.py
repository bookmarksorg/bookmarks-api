from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

class Genre(models.Model):
    id_gender = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name


class Book(models.Model):
    cod_ISBN = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=30, blank=True, null=True)
    blurb = models.TextField(blank=True, null=True)
    published = models.IntegerField(blank=True, null=True)
    number_pages = models.IntegerField(blank=True, null=True)
    cover = models.URLField(blank=True, null=True)
    genres = models.ManyToManyField(Genre, blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title

    @property
    def qty_reviews(self):
        return Review.objects.filter(cod_ISBN=self).count()

    @property
    def qty_discussions(self):
        return Discussion.objects.filter(cod_ISBN=self).count()

    @property
    def rating(self):
        return Review.objects.filter(cod_ISBN=self).aggregate(models.Avg('rating'))['rating__avg'] or 0


class CustomUserModelManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        """
          Creates a custom user with the given fields
        """

        user = self.model(
            username=username,
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password):
        user = self.create_user(
            username,
            email,
            password=password
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user

class Users(AbstractUser, PermissionsMixin):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True, null=True)
    email = models.EmailField(unique=True)
    date_birth = models.DateField(blank=True, null=True)
    points = models.IntegerField(null=True, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)
    favorite_books = models.ManyToManyField(Book, blank=True)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['email']

    active = models.BooleanField(default=True)

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    created = models.DateTimeField('Data Criação', auto_now=False, auto_now_add=True)
    updated = models.DateTimeField('Data Atualização', auto_now=True, auto_now_add=False)

    objects = CustomUserModelManager()

    class Meta:
        ordering = ['username']
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username
    

class Review(models.Model):
    id_review = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.IntegerField()
    date = models.DateTimeField(auto_now_add=True)
    is_adult = models.BooleanField(default=False)
    is_spoiler = models.BooleanField(default=False)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    cod_ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.title
    
    
class Discussion(models.Model):
    id_discussion = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_adult = models.BooleanField(default=False)
    is_spoiler = models.BooleanField(default=False)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    cod_ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Discussions'

    def __str__(self):
        return self.title
    
    @property
    def qty_comments(self):
        return Comments.objects.filter(id_discussion=self).count()
    
    @property
    def qty_likes(self):
        return LikedDiscussions.objects.filter(id_discussion=self).count()
    
    @property
    def qty_tags(self):
        return TaggedDiscussions.objects.filter(id_discussion=self).count()

class TaggedDiscussions(models.Model):
    id_tagged = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    id_discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id_tagged']
        verbose_name_plural = 'Tagged Discussions'

    def __str__(self):
        return str(self.id_tagged)


class LikedDiscussions(models.Model):
    id_liked = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    id_discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id_liked']
        verbose_name_plural = 'Liked Discussions'

    def __str__(self):
        return str(self.id_liked)


class Comments(models.Model):
    id_comment = models.AutoField(primary_key=True)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    id_related_comment = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='child_comments')
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE, null=True, blank=True)
    id_discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE)

    class Meta:
        ordering = ['date']
        verbose_name_plural = 'Comments'

    def __str__(self):
        return str(self.id_comment)

    @property
    def answers(self):
        return self.child_comments.all()

    @property
    def likes(self):
        return LikedComments.objects.filter(id_comment=self.id_comment).count()
    
    @property
    def is_root(self):
        return self.id_related_comment is None
    
    @property
    def author(self):
        return self.id_user.username
    
    @property
    def depth(self):
        depth = 0
        comment = self
        while comment.id_related_comment is not None:
            comment = comment.id_related_comment
            depth += 1
        return depth

class LikedComments(models.Model):
    id_liked = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    id_comment = models.ForeignKey(Comments, on_delete=models.CASCADE)

    class Meta:
        ordering = ['id_liked']
        verbose_name_plural = 'Liked Comments'

    def __str__(self):
        return str(self.id_liked)