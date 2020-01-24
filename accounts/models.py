from django.db import models


class Person(models.Model):
    full_name = models.CharField(max_length=255,)
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.full_name

