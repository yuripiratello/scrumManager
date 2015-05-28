# -*- coding: utf-8 -*-
__author__ = 'yuri'
from models import TaskComment
from django.forms import ModelForm

class CommentForm(ModelForm):
    class Meta:
        model = TaskComment
        fields = '__all__'