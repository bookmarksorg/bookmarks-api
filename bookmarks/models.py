from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin

class Genres(models.Model):
    id_gender = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Genres'

    def __str__(self):
        return self.name

    
class Books(models.Model):
    cod_ISBN = models.CharField(max_length=13, primary_key=True)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=50, blank=True, null=True)
    language = models.CharField(max_length=30, blank=True, null=True)
    blurb = models.TextField(blank=True, null=True)
    published = models.DateTimeField(blank=True, null=True)
    number_pages = models.IntegerField(blank=True, null=True)
    cover = models.URLField(blank=True, null=True)
    genres = models.ManyToManyField(Genres, blank=True)
    rating = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title


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
    genres = models.ManyToManyField(Genres, blank=True)
    favorite_books = models.ManyToManyField(Books, blank=True)

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
    

class Reviews(models.Model):
    id_review = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    rating = models.FloatField()
    date = models.DateField()
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    cod_ISBN = models.ForeignKey(Books, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Reviews'

    def __str__(self):
        return self.title
    
    
class Discussions(models.Model):
    id_discussion = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    cod_ISBN = models.ForeignKey(Books, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Discussions'

    def __str__(self):
        return self.title
    
class TaggedDiscussions(models.Model):
    id_tagged = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Users,  on_delete=models.CASCADE)
    id_discussion = models.ForeignKey(Discussions,  on_delete=models.CASCADE)

    class Meta:
        ordering = ['id_tagged']
        verbose_name_plural = 'Tagged Discussions'

    def __str__(self):
        return str(self.id_tagged)


class LikedDiscussions(models.Model):
    id_liked = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Users,  on_delete=models.CASCADE)
    id_discussion = models.ForeignKey(Discussions,  on_delete=models.CASCADE)

    class Meta:
        ordering = ['id_liked']
        verbose_name_plural = 'Liked Discussions'

    def __str__(self):
        return str(self.id_liked)


class Comments(models.Model):
    id_comment = models.AutoField(primary_key=True)
    description = models.TextField()
    date = models.DateField()
    id_related_comment = models.ForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True)
    id_user = models.ForeignKey(Users, on_delete=models.CASCADE)
    cod_ISBN = models.ForeignKey(Books, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-date']
        verbose_name_plural = 'Comments'

    def __str__(self):
        return str(self.id_comment)
    

class LikedComments(models.Model):
    id_liked = models.AutoField(primary_key=True)
    id_user = models.ForeignKey(Users,  on_delete=models.CASCADE)
    id_discussion = models.ForeignKey(Discussions,  on_delete=models.CASCADE)

    class Meta:
        ordering = ['id_liked']
        verbose_name_plural = 'Liked Comments'

    def __str__(self):
        return str(self.id_liked)