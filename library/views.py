
from django.shortcuts import render, redirect, reverse
from .models import (BookCard,AuthorBookCard, Author, Book,
                     Genre, Account, Librarian, Reader)
from .forms import BookForm, LoginForm, RegisterForm, ObjectBookForm

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
        book_list.append({
            'title': book_card.title,
            'authors': authors,
            'genre': book_card.genre.title,
            'release_year': book_card.release_year,
        })
    return book_list

def librarian_add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            genre_title = form.cleaned_data['genre']
            isbn = form.cleaned_data['isbn']
            author_full_name = form.cleaned_data['author']
            release_year = form.cleaned_data['release_year']
            is_in_reading_room = form.cleaned_data['is_in_reading_room']
            inventory_number = form.cleaned_data['inventory_number']

            genre, _ = Genre.objects.get_or_create(
                title=genre_title
            )
            book_card, _ = BookCard.objects.get_or_create(
                genre=genre,
                title=title,
                isbn=isbn,
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
                in_reading_room=is_in_reading_room,
                inventory_number=inventory_number
            )
            return redirect('./')
        else:
            return render(request, 'lib_add_book.html',
                          {'form': form, 'errors': 'incorrect values'})
    form = BookForm()
    return render(request, 'lib_add_book.html',
                  {'form': form})

def librarian_delete_book(request):
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
                return redirect('./')
            else:
                return render(request, 'lib_del_book.html', data)
        else:
            return render(request, 'lib_del_book.html', data)
    form = BookForm()
    return render(request, 'lib_del_book.html',
                  {'form': form})

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


