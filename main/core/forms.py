from django import forms
from django.core.exceptions import ValidationError
from django.forms import Textarea, CharField, HiddenInput, TextInput, URLInput, SlugField

from .models import Articles


class ArticleForm(forms.ModelForm):

    class Meta:
        model = Articles
        fields = ['name', 'text', 'url']

        # widgets = {
        #     'name': TextInput(attrs={'class': 'form-control-lg'}),
        #     'text': Textarea(attrs={'class': 'form-control'}),
        #     'url': TextInput(attrs={'class': 'form-control'}),
        # }

    # def clean_slug(self):
    #     new_slug = self.cleaned_data['slug']
    #     print("lol")
    #     if ArticleForm.objects.filter(slug__iexact=new_slug).count():
    #         raise ValidationError('slug must be unique. we already have "{}" slug'.format(new_slug))
    #     return new_slug

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = "text name"
        self.fields['name'].widget.attrs['class'] += " form-control-lg"

