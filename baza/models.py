from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=63, primary_key=True)
    # firstname = models.CharField(max_length=255, null=True, blank=True)
    # lastname = models.CharField(max_length=255, null=True, blank=True)
    # username = models.CharField(max_length=255, null=True, blank=True)

    objects = models.Manager()


    def __str__(self):
        return self.user_id


class Book(models.Model):
    title = models.CharField(max_length=127, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.title


class Unit(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=127)

    objects = models.Manager()

    def __str__(self):
        return self.title


class Word(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    word = models.CharField(max_length=127)
    definition = models.CharField(max_length=127, null=True, blank=True)
    tarjima = models.CharField(max_length=127)

    objects = models.Manager()

    def __str__(self):
        return self.word
