
from django.shortcuts import render, redirect
from .models import BookCard,AuthorBookCard, Author, Book, Genre
from .forms import BookForm

def get_books_list():
    book_cards = (
        BookCard.objects
        .select_related('genre')
        .prefetch_related('authorbookcard_set__author')
    )
    book_list = []
    for book_card in book_cards:
        authors = ', '.join([abc.author.full_name for abc in book_card.authorbookcard_set.all()])
        book_list.append({
            'title': book_card.title,
            'authors': authors,
            'genre': book_card.genre.title,
            'release_year': book_card.release_year,
        })
    return book_list

def register(request):
    return render(request, "register.html")

def login(request):
    return render(request, "login.html")

def home(request):
    return render(request, 'index.html', {'books': get_books_list()})

def librarian(request):
    return render(request, 'librarian.html', {'books': get_books_list()})

def reader(request):
    return render(request, 'reader.html', {'books': get_books_list()})

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

            genre, _ = Genre.objects.get_or_create(title=genre_title)
            book_card, _ = BookCard.objects.get_or_create(genre=genre, title=title, isbn=isbn, release_year=release_year)
            author, _ = Author.objects.get_or_create(full_name=author_full_name)
            AuthorBookCard.objects.get_or_create(book_card=book_card, author=author)
            Book.objects.create(book_card=book_card, in_reading_room=is_in_reading_room, inventory_number=inventory_number)

            return redirect('./')
        else:
            return render(request, 'lib_add_book.html', {'form': form, 'errors': 'incorrect values'})

    form = BookForm()
    return render(request, 'lib_add_book.html', {'form': form})


