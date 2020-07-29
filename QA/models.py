from django.db import models
from django.template.defaultfilters import slugify 
from datetime import datetime
from django.utils import timezone
from porsgram.settings import TEMPLATES_DIR

from ckeditor_uploader.fields import RichTextUploadingField 
import re 
import os

from user.models import UserModel



# Create your models here.

'''
    TODO:
        set author on_delete do_nothing 
        on answer and question models 
'''



class QuestionModel(models.Model):
    title        = models.CharField(max_length=200)
    content      = RichTextUploadingField()
    vote_counter = models.SmallIntegerField(default=0)
    author       = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date         = models.DateTimeField(auto_now_add=True)

    objects      = models.Manager()

    class Meta:
        ordering = ['-date',]


    def delete(self, force_insert=False, force_update=False, using=None):
        delete_QA_images(self.content)
        super().delete()


class AnswerModel(models.Model):
    content      = RichTextUploadingField()
    vote_counter = models.SmallIntegerField(default=0)
    approved     = models.BooleanField(default=False)
    question     = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='question')
    author       = models.ForeignKey(UserModel, on_delete=models.DO_NOTHING, related_name='author')    

    objects      = models.Manager()

    class Meta:
        unique_together = ['author', 'question']


    def delete(self, force_insert=False, force_update=False, using=None):
        delete_QA_images(self.content)
        super().delete()



class TagListModel(models.Model):
    tag     = models.CharField(max_length=30, unique=True)
    objects = models.Manager()

class QTagModel(models.Model):
    tag_key      = models.ForeignKey(TagListModel, on_delete=models.CASCADE)
    question_key = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['tag_key', 'question_key']


class QVote(models.Model):
    STATUS_CHOICES = (
        ('like'   , 'like'),
        ('none'   , 'none'),
        ('dislike', 'dislike'),
    )

    user_key        = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    question_key    = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    like_or_dislike = models.CharField(choices=STATUS_CHOICES, default='none', max_length=7)

    class Meta:
        unique_together = ['user_key', 'question_key']


class AVote(models.Model):
    STATUS_CHOICES = (
        ('like'   , 'like'),
        ('none'   , 'none'),
        ('dislike', 'dislike'),
    )

    user_key        = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    answer_key      = models.ForeignKey(AnswerModel, on_delete=models.CASCADE)
    like_or_dislike = models.CharField(choices=STATUS_CHOICES, default='none', max_length=7)

    class Meta:
        unique_together = ['user_key', 'answer_key']



# Special functions
def delete_QA_images(content):
    imgs = re.findall('src="([^"]*)"', content)
    for img in imgs:
        path = TEMPLATES_DIR + img
        if os.path.isfile(path):
            os.remove(path)

