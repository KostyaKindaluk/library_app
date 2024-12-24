from django.contrib import admin
from library.models import (Accounts, Readers, Librarians, Admins, Books, BookCards, BorrowedBooks,
                    AuthorBookCard, Authors, Genres, Reviews)

admin.site.register(Accounts)
admin.site.register(Readers)
admin.site.register(Librarians)
admin.site.register(Admins)
admin.site.register(Books)
admin.site.register(BookCards)
admin.site.register(BorrowedBooks)
admin.site.register(AuthorBookCard)
admin.site.register(Authors)
admin.site.register(Genres)
admin.site.register(Reviews)