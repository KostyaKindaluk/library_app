from django.contrib import admin
from library.models import (Account, Reader, Librarian, Admin, Book, BookCard, BorrowedBook,
                    AuthorBookCard, Author, Genre, Review)

admin.site.register(Account)
admin.site.register(Reader)
admin.site.register(Librarian)
admin.site.register(Admin)
admin.site.register(Book)
admin.site.register(BookCard)
admin.site.register(BorrowedBook)
admin.site.register(AuthorBookCard)
admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Review)