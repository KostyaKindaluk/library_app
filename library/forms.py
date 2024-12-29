from django.forms import (TextInput, EmailInput, PasswordInput, ModelForm,
                          Form, CharField, IntegerField, EmailField, Textarea)
from .models import Account
from django.core.validators import MinValueValidator, MaxValueValidator

class BookForm(Form):
    title = CharField(
                      max_length=200,
                      widget=TextInput(attrs={
                          'class' : 'form-control',
                          'placeholder': 'title'}, )
                      )
    genre = CharField(max_length=100,
                      widget=TextInput(attrs={
                          'class' : 'form-control',
                          'placeholder': 'genre'})
                      )
    author = CharField(max_length=200,
                       widget=TextInput(attrs={
                           'class' : 'form-control',
                           'placeholder': 'author'})
                       )
    release_year = IntegerField(widget=TextInput(attrs={
        'class' : 'form-control',
        'placeholder': 'release year'}),
        validators=[MinValueValidator(1900), MaxValueValidator(2024)]
    )
    inventory_number = IntegerField(widget=TextInput(attrs={
        'class' : 'form-control',
        'placeholder': 'inventory number'}),
    )

class LoginForm(ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'password']
        widgets = {
            'email': EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'email'
            }),
            'password': PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'password'
            })
        }

class RegisterForm(Form):
    fullname = CharField(max_length=255,
                         widget=TextInput(attrs={
                             'class': 'form-control',
                             'placeholder': 'fullname'})
                         )
    email = EmailField(
                      max_length=254,
                      widget=EmailInput(attrs={
                          'class' : 'form-control',
                          'placeholder': 'email'}, )
                      )
    password = CharField(max_length=255,
                      widget=PasswordInput(attrs={
                          'class' : 'form-control',
                          'placeholder': 'password'})
                      )
    phone_number = CharField(max_length=20,
                     widget=TextInput(attrs={
                         'class' : 'form-control',
                         'placeholder': 'phone number'})
                     )
    address = CharField(max_length=200,
                       widget=TextInput(attrs={
                           'class' : 'form-control',
                           'placeholder': 'address'})
                       )

class ObjectBookForm(Form):
    inventory_number = IntegerField(widget=TextInput(attrs={
        'class' : 'form-control',
        'placeholder': 'inventory number'})
    )

class FeedbackForm(Form):
    feedback = CharField(widget=Textarea(attrs={
        'class' : 'form-control',
        'placeholder': 'review'})
    )


