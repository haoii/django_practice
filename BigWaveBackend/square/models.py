from django.db import models


class User(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=20)
    portrait_url = models.CharField(max_length=200)


class SquarePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post_text = models.CharField(max_length=280)
    image_url = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    pub_date = models.DateTimeField('date published')



