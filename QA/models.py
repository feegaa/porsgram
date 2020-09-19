from django.db import models
from django.template.defaultfilters import slugify 
from datetime import datetime
from django.utils import timezone
from django import template
from django.shortcuts import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.apps import apps


from porsgram.settings import TEMPLATES_DIR, MEDIA_URL

from ckeditor_uploader.fields import RichTextUploadingField 
import jdatetime as jdt
import re 
import os


'''
    TODO:
        set author on_delete do_nothing 
        on answer and question models 
'''

register = template.Library()


class QuestionModel(models.Model):
    title      = models.CharField(max_length=200)
    content    = RichTextUploadingField()
    vote       = models.SmallIntegerField(default=0)
    author     = models.ForeignKey(to="user.UserModel", on_delete=models.CASCADE)
    date       = models.DateTimeField(auto_now_add=True)
    review     = models.PositiveSmallIntegerField(default=0)
    answers_NO = models.PositiveSmallIntegerField(default=0)
    edited     = models.BooleanField(default=False)

    objects      = models.Manager()

    class Meta:
        ordering = ['-date',]


    def delete(self, force_insert=False, force_update=False, using=None):
        deleteQAImages(self.content)
        super().delete()

    @register.filter(name="getVoteUrl")
    def getVoteUrl(self):
        return reverse('QA:question_vote')

    @register.filter(name="getVoteNO")
    def getVoteNO(self):
        self.setVoteNO()
        return self.vote

    def setVoteNO(self):
        self.vote = 0
        likes     = QVote.objects.filter(question=self, like_or_dislike=True).count()
        dislikes  = QVote.objects.filter(question=self, like_or_dislike=False).count()
        self.vote = likes - dislikes
        self.save()

    @register.filter(name="getApprovedAnswerId")
    def getApprovedAnswerId(self):
        try:
            result = list(AnswerModel.objects.filter(question=self).values_list('id', flat=True))
        except ObjectDoesNotExist:
            result = None
        return result


    @register.filter(name="getTags")
    def getTags(self):
        try:
            tags = QTagModel.objects.filter(question=self)
            tags = [i.tag for i in tags]
            # tags    = list(TagListModel.objects.filter(id__in=tags_id))
        except ObjectDoesNotExist:
            tags    = None
        return tags
        

    @register.filter(name="getDate")
    def getDate(self):
        jdt.set_locale('fa_IR')
        return jdt.datetime.fromgregorian(date=self.date).strftime('%H:%M %Y %B %d')


class AnswerModel(models.Model):
    content     = RichTextUploadingField()
    vote        = models.SmallIntegerField(default=0)
    question    = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, related_name='question')
    author      = models.ForeignKey(to="user.UserModel", on_delete=models.DO_NOTHING, related_name='author')    
    is_approved = models.BooleanField(default=False)
    edited      = models.BooleanField(default=False)
    date        = models.DateTimeField(auto_now_add=True)

    objects      = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'author'], name='answer')
        ]


    def delete(self, force_insert=False, force_update=False, using=None):
        deleteQAImages(self.content)
        super().delete()


    def setVoteNO(self):
        self.vote = 0
        likes     = AVote.objects.filter(answer=self, like_or_dislike=True).count()
        dislikes  = AVote.objects.filter(answer=self, like_or_dislike=False).count()
        self.vote = likes - dislikes
        self.save()


    @register.filter(name="getVoteUrl")
    def getVoteUrl(self):
        return reverse('QA:answer_vote')


    @register.filter(name="getAnswerApproveUrl")
    def getAnswerApproveUrl(self):
        return reverse('QA:answer_approved')


    @register.filter(name="isApproved")
    def isApproved(self):
        path = MEDIA_URL + "images/" + ("green.png" if self.is_approved else "gray.png")
        return path


    @register.filter(name="getVoteNO")
    def getVoteNO(self):
        self.setVoteNO()
        return self.vote


    @register.filter(name="getDate")
    def getDate(self):
        jdt.set_locale('fa_IR')
        return jdt.datetime.fromgregorian(date=self.date).strftime('%H:%M %Y %B %d')


class CommentModel(models.Model):
    comment  = models.CharField(max_length=500)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    author   = models.ForeignKey(to='user.UserModel', on_delete=models.CASCADE)
    date     = models.DateTimeField(auto_now_add=True)
    
    objects  = models.Manager()

    @register.filter(name="getDate")
    def getDate(self):
        jdt.set_locale('fa_IR')
        return jdt.datetime.fromgregorian(date=self.date).strftime('%H:%M %Y %B %d')


class TagListModel(models.Model):
    tag     = models.CharField(max_length=30, unique=True)
    objects = models.Manager()

class QTagModel(models.Model):
    tag      = models.ForeignKey(TagListModel, on_delete=models.CASCADE)
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    objects  = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'tag'], name='qtag')
        ]


class QVote(models.Model):

    user            = models.ForeignKey(to="user.UserModel", on_delete=models.CASCADE)
    question        = models.ForeignKey(QuestionModel, on_delete=models.CASCADE)
    like_or_dislike = models.BooleanField(default=False, blank=False)
    
    objects         = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['question', 'user'], name='qvote')
        ]



class AVote(models.Model):

    user            = models.ForeignKey(to="user.UserModel", on_delete=models.CASCADE)
    answer          = models.ForeignKey(AnswerModel, on_delete=models.CASCADE)
    like_or_dislike = models.BooleanField(default=False, blank=False)
    
    objects         = models.Manager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['answer', 'user'], name='avote')
        ]


class AnswerApproved(models.Model):
    answer   = models.ForeignKey(AnswerModel, on_delete=models.CASCADE)
    question = models.OneToOneField(QuestionModel, 
                                    on_delete=models.CASCADE, 
                                    primary_key=True, 
                                    related_name="answer_approved")

    objects  = models.Manager() 


# Special functions
def deleteQAImages(content):
    imgs = re.findall('src="([^"]*)"', content)
    for img in imgs:
        path = TEMPLATES_DIR + img
        if os.path.isfile(path):
            os.remove(path)

