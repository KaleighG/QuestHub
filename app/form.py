from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from app.models import *
from django import forms



# Create your models here.
class CreateUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class CreatePostForm(ModelForm):
    class Meta:
        model = Post
        fields = ["image", "caption"]

    def __init__(self, *args, **kwargs):
        super(CreatePostForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({"class": "form-control"})


class PostSearchForm(forms.Form):
    query = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'placeholder': 'Search posts...'}))

class ChatGPTForm(forms.Form):
    input_text = forms.CharField(label='Input Text', widget=forms.Textarea)