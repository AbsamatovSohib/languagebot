from django.contrib import admin
from baza.models import Book, Unit, Word, User


admin.site.register(User)
admin.site.register(Book)
admin.site.register(Unit)
admin.site.register(Word)
