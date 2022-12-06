from django import forms
from .models import Games, Publishers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Publisher form used to upload a new publisher to the database
class PublisherForm(forms.ModelForm):
  
    # Meta class
    class Meta:
        model = Publishers
        fields = ['publisherName', 'publisherDescription', 'publisherImage']

        widgets = {
            'publisherName': forms.TextInput(attrs = {
            'class': 'form-control', # Turns the field into a bootstrap item
            'placeholder': 'Publisher Name',
            }),

            'publisherDescription': forms.Textarea(attrs = {
            'class': 'form-control', # Bootstrap
            'placeholder': 'Publisher Description',
            'rows' : 25,
            'cols' : 60,
            }),

            }
        

# Game form used to upload a new game to the database, requires a publisher!
class GameForm(forms.ModelForm):

    # create meta class

    class Meta:
    # specify model to be used
        model = Games
        fields = ['title', 'description', 'cheatData', 'gamePublisher', 'coverImage']

        widgets = {
        'title': forms.TextInput(attrs={
        'class': 'form-control', # Bootstrap
        'placeholder': 'Game Title',
        }),

        'description': forms.Textarea(attrs={
        'class': 'form-control', # Bootstrap
        'placeholder': 'Game Description',
        'rows' : 25,
        'cols' : 60,
        }),

        'cheatData': forms.Textarea(attrs={
        'class': 'form-control', # Bootstrap
        'placeholder': 'List cheats here...',
        'rows' : 25,
        'cols' : 60,

        }),

        }

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True, label = 'Email')

    class Meta:
        model = User
        fields = ("username", "email")