from django.forms import ModelForm 

from .models import Posts

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