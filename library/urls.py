from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('librarian/', views.librarian, name='librarian'),
    path('librarian/add_book/', views.librarian_add_book, name='lib_add_book'),
    path('librarian/delete_book/', views.librarian_delete_book, name='lib_del_book'),
    path('librarian/logout/', views.logout, name='logout'),
    path('reader/', views.reader, name='reader'),
    path('librarian/readers/', views.readers, name='readers'),
    path('reader/borrowing/', views.booking, name='borrowing'),
    path('reader/review/', views.review, name='review'),
    path('librarian/feedback/', views.feedback, name='feedback')
]


