from django.db import models

class Genres(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class BookCards(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    isbn = models.CharField(max_length=18)
    release_year = models.IntegerField()

    def __str__(self):
        return self.title


class Authors(models.Model):
    full_name = models.CharField(max_length=30)

    def __str__(self):
        return self.full_name


class AuthorBookCard(models.Model):
    book_card = models.ForeignKey(BookCards, on_delete=models.CASCADE)
    author = models.ForeignKey(Authors, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.book_card} by {self.author}'


class Accounts(models.Model):
    email = models.EmailField(max_length=254)
    password_hash = models.CharField(max_length=255)


class Readers(models.Model):
    account = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    passport_series = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    birthday = models.DateField()
    creation_date = models.DateField(auto_now_add=True)
    work_place = models.CharField(max_length=100)
    job_title = models.CharField(max_length=100)

    def __str__(self):
        return self.fullname


class Librarians(models.Model):
    account = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    passport_series = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    hire_date = models.DateField()

    def __str__(self):
        return self.fullname


class Admins(models.Model):
    account = models.OneToOneField(Accounts, on_delete=models.CASCADE)
    fullname = models.CharField(max_length=150)
    passport_series = models.CharField(max_length=10, unique=True)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    hire_date = models.DateField()

    def __str__(self):
        return self.fullname


class Books(models.Model):
    book_card = models.ForeignKey(BookCards, on_delete=models.CASCADE)
    in_reading_room = models.BooleanField()
    inventory_number = models.IntegerField(unique=True)

    def __str__(self):
        return self.book_card.title


class Reviews(models.Model):
    book_card = models.ForeignKey(BookCards, on_delete=models.CASCADE)
    reader = models.ForeignKey(Readers, on_delete=models.CASCADE)
    rating = models.IntegerField()
    comment = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Review for {self.book_card.title}'


class BorrowedBooks(models.Model):
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    reader = models.ForeignKey(Readers, on_delete=models.CASCADE)
    librarian = models.ForeignKey(Librarians, on_delete=models.CASCADE)
    borrow_date = models.DateField()
    return_until_date = models.DateField()

    def __str__(self):
        return f'{self.book} borrowed by {self.reader}'