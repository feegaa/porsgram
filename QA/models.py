from django.db import models
from django.template.defaultfilters import slugify 
from datetime import datetime
from django.utils import timezone
from django import template
from django.shortcuts import reverse

from porsgram.settings import TEMPLATES_DIR

from ckeditor_uploader.fields import RichTextUploadingField 
import re 
import os

from user.models import UserModel




'''
    TODO:
        set author on_delete do_nothing 
        on answer and question models 
'''

register = template.Library()


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

    @register.filter(name="getVoteUrl")
    def getVoteUrl(self):
        return reverse('QA:question_vote')

    @register.filter(name="getVoteState")
    def getVoteState(self):
        likes    = QVote.objects.filter(question=self, like_or_dislike=True).count()
        dislikes = QVote.objects.filter(question=self, like_or_dislike=False).count()
        return likes - dislikes


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


    @register.filter(name="getVoteUrl")
    def getVoteUrl(self):
        return reverse('QA:answer_vote')


    @register.filter(name="getVoteState")
    def getVoteState(self):
        likes    = AVote.objects.filter(answer=self, like_or_dislike=True).count()
        dislikes = AVote.objects.filter(answer=self, like_or_dislike=False).count()
        return likes - dislikes


class TagListModel(models.Model):
    tag     = models.CharField(max_length=30, unique=True)
    objects = models.Manager()

class QTagModel(models.Model):
    tag      = models.ForeignKey(TagListModel, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    objects  = models.Manager()

    class Meta:
        unique_together = ['tag', 'question']


class QVote(models.Model):

    user            = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    question        = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    like_or_dislike = models.BooleanField(default=False, blank=False)
    
    objects         = models.Manager()

    class Meta:
        unique_together = ['user', 'question']



class AVote(models.Model):

    user            = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    answer          = models.ForeignKey(AnswerModel, on_delete=models.CASCADE)
    like_or_dislike = models.BooleanField(default=False, blank=False)
    
    objects         = models.Manager()

    class Meta:
        unique_together = ['user', 'answer']



# Special functions
def delete_QA_images(content):
    imgs = re.findall('src="([^"]*)"', content)
    for img in imgs:
        path = TEMPLATES_DIR + img
        if os.path.isfile(path):
            os.remove(path)

