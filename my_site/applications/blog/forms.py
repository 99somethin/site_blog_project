from django import forms
from .models import CommentModel


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25, required=True,
                           widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Name'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'E-Mail'}))
    send_to_email = forms.EmailField(required=True, widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'To'}))
    comments = forms.CharField(required=False,
                               widget=forms.Textarea(attrs={"class": "form-control mb-1", 'placeholder': 'Comments'}))


class CommentForm(forms.ModelForm):
    name = forms.CharField(required=True,
                           widget=forms.TextInput(attrs={"class": "form-control", 'placeholder': 'Name'}))
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={"class": "form-control", 'placeholder': 'Email'}))
    body = forms.CharField(required=True, widget=forms.Textarea(attrs={"class": "form-control", 'placeholder': 'Text'}))

    class Meta:
        model = CommentModel
        fields = ['name', 'email', 'body']


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100,
                            widget=forms.TextInput(attrs={"class": "form-control mb-1", 'placeholder': 'Enter search term...'}))