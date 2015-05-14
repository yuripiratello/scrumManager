__author__ = 'yuri'
from models import TaskComment
from django.forms import ModelForm

class CommentForm(ModelForm):
    class Meta:
        model = TaskComment