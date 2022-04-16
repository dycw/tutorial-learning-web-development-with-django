from django.db.models import CharField
from django.db.models import Model


class Book(Model):
    name = CharField(max_length=255)
    author = CharField(max_length=50)
