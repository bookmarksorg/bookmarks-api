from django.db import models


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
    author = models.CharField(max_length=50)
    language = models.CharField(max_length=30)
    blurb = models.TextField()
    published = models.DateTimeField()
    number_pages = models.IntegerField()
    cover = models.FileField()
    genres = models.ManyToManyField(Genres)
    rating = models.FloatField(null=True, blank=True)

    class Meta:
        ordering = ['title']
        verbose_name_plural = 'Books'

    def __str__(self):
        return self.title
    

class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30)
    description = models.TextField()
    email = models.EmailField(unique=True)
    date_birth = models.DateField()
    points = models.IntegerField(null=True, blank=True)
    genres = models.ManyToManyField(Genres)
    favorite_books = models.ManyToManyField(Books)

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