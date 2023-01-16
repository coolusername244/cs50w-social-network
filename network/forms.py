from django import forms
from django.forms import ModelForm 

from .models import Posts, UserInfo

class PostForm(ModelForm):
    class Meta:
        model = Posts
        fields = [
            "post",
        ]
        labels = {
            "post": ""
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # style form fields
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control mb-3'
            field.widget.attrs['rows'] = '5'


class UserInfoForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = [
            "location",
            "profile_pic",
            "birthday",
            "bio",
        ]

        widgets = {
            "profile_pic" : forms.FileInput(
                attrs={
                    "class":"form-control"
                }),
            "birthday" : forms.DateInput(
                attrs={
                    "class":"form-control",
                    "type":"date"
                }),
            "location" : forms.TextInput(
                attrs={
                    "class": "autocomplete-input",
                }),
            "bio": forms.Textarea(
                attrs={
                    "class":"form-control",
                    "rows": "5"
                }),
        }
        
