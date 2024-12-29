
from django.shortcuts import render, redirect
from django.db.models import Count
from .models import (BookCard,AuthorBookCard, Author, Book, Review,
                     Genre, Account, Librarian, Reader, BorrowedBook)
from .forms import BookForm, LoginForm, RegisterForm, ObjectBookForm, FeedbackForm

def get_books_list():
    book_cards = (
        BookCard.objects
        .select_related('genre')
        .prefetch_related('authorbookcard_set__author')
    )
    book_list = []
    for book_card in book_cards:
        authors = ', '.join(
            [abc.author.full_name for abc in book_card.authorbookcard_set.all()]
        )
        book = Book.objects.get(book_card=book_card)
        book_list.append({
            'title': book_card.title,
            'authors': authors,
            'genre': book_card.genre.title,
            'release_year': book_card.release_year,
            'inventory_number': book.inventory_number
        })
    return book_list

def librarian_add_book(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'librarian':
        return redirect("login")
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            if BookCard.objects.filter(title=title).exists():
                return render(request, 'lib_add_book.html',
                              {'form': form, 'errors': 'title must be unique'})
            genre_title = form.cleaned_data['genre']
            author_full_name = form.cleaned_data['author']
            release_year = form.cleaned_data['release_year']
            inventory_number = form.cleaned_data['inventory_number']
            if Book.objects.filter(inventory_number=inventory_number).exists():
                return render(request, 'lib_add_book.html',
                              {'form': form, 'errors': 'inventory number must be unique'})
            genre, _ = Genre.objects.get_or_create(
                title=genre_title
            )
            try:
                book_card, _ = BookCard.objects.get_or_create(
                    genre=genre,
                    title=title,
                    release_year=release_year)
                author, _ = Author.objects.get_or_create(
                    full_name=author_full_name
                )
                AuthorBookCard.objects.get_or_create(
                    book_card=book_card,
                    author=author
                )
                Book.objects.create(
                    book_card=book_card,
                    inventory_number=inventory_number
                )
            except BaseException as er:
                return render(request, 'lib_add_book.html',
                              {'form': form, 'errors': er})
            return redirect('../')
        else:
            return render(request, 'lib_add_book.html',
                          {'form': form, 'errors': 'incorrect values'})
    form = BookForm()
    acc = Account.objects.filter(pk=request.session.get('user_id'))
    return render(request, 'lib_add_book.html',
                  {'form': form, 'account': acc})

def librarian_delete_book(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'librarian':
        return redirect("login")
    acc = Account.objects.get(pk=request.session.get('user_id'))
    if request.method == 'POST':
        form = ObjectBookForm(request.POST)
        data = {
            'form': form,
            'errors': 'there is no book with such inventory number'
        }
        if form.is_valid():
            inventory_number = form.cleaned_data['inventory_number']
            if Book.objects.filter(inventory_number=inventory_number).exists():
                book = Book.objects.get(inventory_number=inventory_number)
                bookCard = book.book_card
                title = bookCard.title
                genre = bookCard.genre
                release_year = bookCard.release_year
                book.delete()
                if not Book.objects.filter(book_card=bookCard).exists():
                    genre = bookCard.genre
                    authorBookCards = AuthorBookCard.objects.filter(book_card=bookCard)
                    authors = []
                    for authorBookCard in authorBookCards:
                        authors.append(authorBookCard.author)
                    bookCard.delete()
                    for author in authors:
                        if not AuthorBookCard.objects.filter(author=author).exists():
                            Author.objects.filter(full_name=author).delete()
                    if not BookCard.objects.filter(genre=genre).exists():
                        Genre.objects.filter(title=genre).delete()

                if BorrowedBook.objects.filter(
                        genre=genre, title=title, release_year=release_year).exists():
                    BorrowedBook.objects.filter(
                        genre=genre, title=title, release_year=release_year).delete()

                return redirect('../')
            else:
                return render(request, 'lib_del_book.html', data)
        else:
            return render(request, 'lib_del_book.html', data)
    form = BookForm()
    return render(request, 'lib_del_book.html',
                  {'form': form, 'account': acc})

def home(request):
    return render(request, 'index.html',
                  {'books': get_books_list()})

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            fullname = form.cleaned_data['fullname']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            phone_number = form.cleaned_data['phone_number']
            for ch in phone_number:
                if not ch.isdigit():
                    return render(request, "register.html",
                                  {
                                      'form': form,
                                      'errors': 'phone number must consist of numbers only'
                                  })
            address = form.cleaned_data['phone_number']
            if (not Account.objects.filter(email=email).exists() and
                    not Reader.objects.filter(phone_number=phone_number).exists()):
                account = Account(email=email, password=password)
                account.save()
                reader = Reader(
                    account=account,
                    fullname=fullname,
                    address=address,
                    phone_number=phone_number,
                )
                reader.save()
                return redirect("../", {'reader': reader})
            else:
                return render(request, "register.html",
        {
                'form': form,
                'errors': ' user with such email or phone number is already exists'
                })

    form = RegisterForm()
    return render(request, "register.html",
                  {'form': form})

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            try:
                Account.objects.get(email=email, password=password)
            except Account.DoesNotExist:
                data = { 'errors': 'Check email and password again', 'form': form }
                return render(request, "login.html", data)
            account = Account.objects.get(email=email, password=password)

            request.session['user_id'] = account.id
            request.session['user_type'] = 'reader' if hasattr(account, 'reader') else 'librarian'

            data = {'books': get_books_list()}
            if hasattr(account, 'reader'):
                return redirect("../reader",data)
            elif hasattr(account, 'librarian'):
                return redirect("../librarian", data)
        else:
            return render(request, "login.html",
                          {'errors': 'Form is not valid', 'form': form})
    form = LoginForm()
    return render(request, "login.html", { 'form': form })

def librarian(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'librarian':
        return redirect("login")
    lib = Librarian.objects.filter(account=request.session.get('user_id'))
    acc = Account.objects.filter(pk=request.session.get('user_id'))
    return render(request, 'librarian.html',
                  {
                            'books': get_books_list(),
                            'librarian': lib,
                            'account': acc
                          })

def reader(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'reader':
        return redirect("login")
    read = Reader.objects.filter(account=request.session.get('user_id'))
    acc = Account.objects.filter(pk=request.session.get('user_id'))
    return render(request, 'reader.html',
                  {
                            'books': get_books_list(),
                            'reader': read,
                            'account': acc
                          })

def logout(request):
    request.session.flush()
    return redirect('../')

def readers(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'librarian':
        return redirect("login")
    acc = Account.objects.filter(pk=request.session.get('user_id'))
    elements = []
    for borrowedBook in BorrowedBook.objects.all():
        bookCard = BookCard.objects.get(title=borrowedBook.title)
        book = Book.objects.filter(book_card=bookCard).first()
        elements.append(f'{borrowedBook.reader.account.email} wants to borrow {borrowedBook.title} (inventory number: {book.inventory_number})')
    return render(request, 'readers.html',
                  {'account': acc, 'elements': elements})

def booking(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'reader':
        return redirect("login")
    acc = Account.objects.filter(pk=request.session.get('user_id'))
    if request.method == 'POST':
        form = ObjectBookForm(request.POST)
        if form.is_valid():
            inventory_number = form.cleaned_data['inventory_number']
            try:
                borrowed_books = BorrowedBook.objects.values('reader').annotate(count=Count('reader'))
                reader = Reader.objects.filter(account=acc[0]).first()
                print(reader)
                for entry in borrowed_books:
                    print(entry)
                    if entry['count'] >= 3 and reader.id == entry['reader']:
                        return render(request, 'booking.html',
                                      {'account': acc,
                                       'form': form,
                                       'errors': 'You can\'t borrow more than 3 books'})
                book = Book.objects.get(inventory_number=inventory_number)
                bookCard = book.book_card
                if BorrowedBook.objects.filter(title=bookCard.title).exists():
                    raise BaseException()
                authorBookCards = AuthorBookCard.objects.filter(book_card=bookCard)
                authors = ''
                for authorBookCard in authorBookCards:
                    authors += authorBookCard.author.full_name
                    authors += ', '
                authors = authors[:-2]
                if not BorrowedBook.objects.filter(reader=Reader.objects.get(account=acc.first()),
                                            title=bookCard.title,
                                            genre=bookCard.genre,
                                            authors=authors,
                                            release_year=bookCard.release_year).exists():
                    BorrowedBook.objects.create(
                        reader=Reader.objects.get(account=acc.first()),
                        title=bookCard.title,
                        genre=bookCard.genre,
                        authors=authors,
                        release_year=bookCard.release_year
                    )
                else:
                    raise BaseException()

                return redirect('../')
            except BaseException as er:
                print(er)
                return render(request, 'booking.html',
                              {'account': acc, 'form': form,
                               'errors': 'There is no such book or it\'s already borrowed'})

        else:
            return render(request, 'booking.html',
                          {'account': acc, 'form': form,
                           'errors': 'There is no such book or it\'s already borrowed'})

    form = ObjectBookForm()
    return render(request, 'booking.html',
                  {'account': acc, 'form': form})

def review(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'reader':
        return redirect("login")
    acc = Account.objects.filter(pk=request.session.get('user_id'))
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.cleaned_data['feedback']
            reader = Reader.objects.get(account=acc.first())
            if not Review.objects.filter(reader=reader).exists():
                Review.objects.create(reader=reader, feedback=feedback)
                return redirect('../')
            else:
                return render(request, 'feedback.html',
                              {'account': acc, 'form': form,
                               'errors': 'you can\'t leave any more reviews'})
    form = FeedbackForm()
    return render(request, 'feedback.html',
                  {'account': acc, 'form': form})

def feedback(request):
    if 'user_id' not in request.session or request.session.get('user_type') != 'librarian':
        return redirect("login")
    acc = Account.objects.filter(pk=request.session.get('user_id'))
    elements = []
    for review in Review.objects.all():
        elements.append(f'{review.reader.fullname}: {review.feedback}')
    return render(request, 'lib_feedback.html',
                  {'account': acc, 'elements': elements})
