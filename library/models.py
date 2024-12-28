from django.db import models

class Genre(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class BookCard(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    isbn = models.CharField(max_length=18)
    release_year = models.IntegerField()

    def __str__(self):
        return self.title


class Author(models.Model):
    full_name = models.CharField(max_length=30)

    def __str__(self):
        return self.full_name


class AuthorBookCard(models.Model):
    book_card = models.ForeignKey(BookCard, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.book_card} by {self.author}'


class Account(models.Model):
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)


class Reader(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    birthday = models.DateField(null=True, blank=True)
    passport_series = models.CharField(max_length=10, unique=True, blank=True, null=True)
    creation_date = models.DateField(null=True, blank=True)
    work_place = models.CharField(max_length=100, null=True, blank=True)
    job_title = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.fullname


class Librarian(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    passport_series = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    hire_date = models.DateField()

    def __str__(self):
        return self.fullname


class Admin(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    passport_series = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    hire_date = models.DateField()

    def __str__(self):
        return self.fullname


class Book(models.Model):
    book_card = models.ForeignKey(BookCard, on_delete=models.CASCADE)
    in_reading_room = models.BooleanField()
    inventory_number = models.IntegerField(unique=True)

    def __str__(self):
        return self.book_card.title


class Review(models.Model):
    book_card = models.ForeignKey(BookCard, on_delete=models.CASCADE)
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Review for {self.book_card.title}'


class BorrowedBook(models.Model):
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True)
    authors = models.CharField(max_length=200, null=True)
    genre = models.CharField(max_length=200, null=True)
    release_year = models.IntegerField(null=True)

    def __str__(self):
        return f'{self.title}, {self.genre}'
