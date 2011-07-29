__author__ = 'yuri'
from models import SprintTaskComment
from django.forms import ModelForm

class CommentForm(ModelForm):
    class Meta:
        model = SprintTaskComment
        fields = ('comment', 'created_by')