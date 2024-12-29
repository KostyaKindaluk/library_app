from django.contrib import admin
from library.models import (Account, Reader, Librarian, Admin, Book, BookCard, BorrowedBook,
                    AuthorBookCard, Author, Genre, Review)

admin.site.register(Account)
admin.site.register(Librarian)


