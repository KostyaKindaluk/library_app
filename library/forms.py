from django import forms
from django.forms import TextInput

class BookForm(forms.Form):
    title = forms.CharField(max_length=200, widget=TextInput(attrs={'class' : 'form-control', 'placeholder': 'title'}, ))
    genre = forms.CharField(max_length=100, widget=TextInput(attrs={'class' : 'form-control', 'placeholder': 'genre'}))
    isbn = forms.CharField(max_length=20, widget=TextInput(attrs={'class' : 'form-control', 'placeholder': 'isbn'}))
    author = forms.CharField(max_length=200, widget=TextInput(attrs={'class' : 'form-control', 'placeholder': 'author'}))
    release_year = forms.IntegerField(widget=TextInput(attrs={'class' : 'form-control', 'placeholder': 'release year'}))
    inventory_number = forms.IntegerField(widget=TextInput(attrs={'class' : 'form-control', 'placeholder': 'inventory number'}))
    is_in_reading_room = forms.BooleanField(widget=TextInput(attrs={'class' : 'form-control', 'placeholder': 'is in reading room ? (0 / 1 - false / true)'}))



