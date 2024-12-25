from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('librarian/', views.librarian, name='librarian'),
    path('librarian/add_book', views.librarian_add_book, name='lib_add_book'),
]


