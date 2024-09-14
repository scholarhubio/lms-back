from django.contrib import admin
from .models.task import Task
from django import forms
from ckeditor.widgets import CKEditorWidget


class MyModelForm(forms.ModelForm):
    text = forms.CharField(widget=CKEditorWidget(config_name='default'))

    class Meta:
        model = Task
        fields = '__all__'
