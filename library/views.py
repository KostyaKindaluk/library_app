from django.shortcuts import render

def register(request):
    return render(request, "register.html")

def login(request):
    return render(request, "login.html")

def home(request):
    return render(request, 'index.html')

def librarian(request):
    return render(request, 'librarian.html')

def librarian_add_book(request):
    return render(request, 'lib_add_book.html')



