from django.db import models
from .validators import file_size


# Create your models here.
class user(models.Model):
    fname = models.CharField(max_length=100, null=False, blank=False)
    lname = models.CharField(max_length=100, null=False, blank=False)
    email = models.CharField(max_length=100, null=False, blank=False)
    password = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return self.fname


class category(models.Model):
    cname = models.CharField(max_length=100, null=True, blank=False)

    def __str__(self):
        return self.cname


class movie_details(models.Model):
    title = models.CharField(max_length=100, null=True, blank=False)
    poster = models.ImageField(upload_to="video/%y", validators=[file_size], null=True)
    description = models.CharField(max_length=100, null=True)
    rdate = models.CharField(max_length=100, null=True)
    actors = models.CharField(max_length=100, null=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE, null=True)
    video = models.CharField(max_length=300, null=True)
    user = models.ForeignKey(user, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

class Review(models.Model):

    movie_details = models.ForeignKey(movie_details, on_delete=models.CASCADE)
    subject = models.TextField(max_length=300, blank=True)
    comment = models.TextField(max_length=300, blank=True)
    rating = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self. subject

