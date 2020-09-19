from porsgram.settings import MEDIA_ROOT
from user.statics import * 
from QA.models import QuestionModel, AnswerModel, AnswerApproved

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django import template
from django.utils.timezone import now


from PIL import Image
from pathlib import Path
import jdatetime as jdt
from ckeditor.fields import RichTextField 


import os


# Create your models here.

register = template.Library()



class UserModel(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = (
        ('female', 'مونث'),
        ('male', 'مذکر'),
        ('none', 'به تو چه'),
    )

    id           = models.AutoField(primary_key=True)
    first_name   = models.CharField(max_length=20, blank=False)
    last_name    = models.CharField(max_length=20, blank=True)
    password     = models.CharField(max_length=100)
    username     = models.CharField(max_length=30, unique=True, blank=False)
    email        = models.EmailField(unique=True, blank=False)
    join_date    = models.DateField(auto_now_add=True)
    last_visit   = models.DateTimeField(auto_now_add=True)
    reputation   = models.PositiveIntegerField(default=0)
    is_staff     = models.BooleanField(default=False)
    gender       = models.CharField(max_length=6, choices=STATUS_CHOICES, default='none')
    is_active    = models.BooleanField(default=False)
    about_me     = RichTextField(null=True, blank=True, max_length=700)
    answers_no   = models.PositiveSmallIntegerField(default=0)
    questions_no = models.PositiveSmallIntegerField(default=0)

    # objects       = models.Manager()
    objects    = UserManager()

    USERNAME_FIELD  = 'username'
    PASSWORD_FIELD  = 'password'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['-reputation']


    @register.filter(name="getDate")
    def getDate(self):
        jdt.set_locale('fa_IR')
        jd    = jdt.date.fromgregorian(date=self.join_date).strftime('%d %B  %Y')
        lv    = jdt.datetime.fromgregorian(date=self.last_visit).strftime('%H:%M %d %B  %Y')
        dates = {'jd': jd, 'lv': lv}
        return dates

    @register.filter(name="getReputation")
    def getReputation(self):
        self.setReputation()
        return self.reputation

    def setReputation(self):
        self.reputation  = 0
        answers          = AnswerModel.objects.filter(author=self)
        questions_NO     = QuestionModel.objects.filter(author=self).count()
        self.reputation += questions_NO * NEW_QUESTION
        self.reputation += answers.count() * NEW_ANSWER
        for answer in answers:
            try:
                AnswerApproved.objects.get(answer=answer)
                self.reputation += APPROVED_ANSWER
            except ObjectDoesNotExist:
                pass
        self.save()
        

    @register.filter(name='getQuestions')
    def getQuestions(self):
        try:
            questions         = QuestionModel.objects.filter(author=self)
            self.questions_no = questions.count()
            self.save()
        except ObjectDoesNotExist:
            questions = None
        return questions



    @register.filter(name='getAnswers')
    def getAnswers(self):
        try:
            answers         = AnswerModel.objects.filter(author=self)
            self.answers_no = answers.count()
            self.save()
        except ObjectDoesNotExist:
            answers = None
        return answers







class AvatarModel(models.Model):
    user    = models.OneToOneField(UserModel, on_delete=models.CASCADE)
    avatar  = models.ImageField(default='default.png', upload_to='avatar')
    objects = models.Manager()


    # def save(self, is_update):
    def save(self, force_insert=False, force_update=False, using=None):
        super().save()
        SIZE       = 225
        FILE_SCALE = (SIZE, SIZE)

        img = Image.open(self.avatar.path)

        if img.width > SIZE or img.height > SIZE:
            img.thumbnail(FILE_SCALE)
            img.save(self.avatar.path)




class SetLastVisitMiddleware(object):
    def process_response(self, request, response):
        if request.user.is_authenticated():
            # Update last visit time after request finished processing.
            UserModel.objects.filter(id=request.user.id).update(last_visit=now())
        return response