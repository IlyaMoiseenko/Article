from django.db import models
from django.contrib.auth.models import User


class Article(models.Model):
    title = models.CharField(max_length=200,
                             null=False,
                             default='')

    text = models.TextField(max_length=1000,
                            null=False,
                            default='')

    create_date = models.DateField(auto_now=True)

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    article = models.ForeignKey('Article',
                                on_delete=models.CASCADE,
                                blank=True,
                                null=True)

    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               blank=True,
                               null=True)

    create_date = models.DateTimeField(auto_now=True)

    text = models.TextField()

    status = models.BooleanField(default=False)