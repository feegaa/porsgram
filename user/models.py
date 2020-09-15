from porsgram.settings import MEDIA_ROOT
from user.statics import * 
from QA.models import QuestionModel, AnswerModel, AnswerApproved

from django.db import models
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import AbstractBaseUser, UserManager, PermissionsMixin
from django import template

from PIL import Image
from pathlib import Path
import jdatetime as jdt

import os


# Create your models here.

register = template.Library()



class UserModel(AbstractBaseUser, PermissionsMixin):
    STATUS_CHOICES = (
        ('female', 'مونث'),
        ('male', 'مذکر'),
        ('none', 'به تو چه'),
    )

    id         = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=20, blank=False)
    last_name  = models.CharField(max_length=20, blank=True)
    password   = models.CharField(max_length=100)
    username   = models.CharField(max_length=30, unique=True, blank=False)
    email      = models.EmailField(unique=True, blank=False)
    join_date  = models.DateField(auto_now_add=True)
    last_seen  = models.DateTimeField(auto_now_add=True)
    reputation = models.PositiveIntegerField(default=0)
    is_staff   = models.BooleanField(default=False)
    gender     = models.CharField(max_length=6, choices=STATUS_CHOICES, default='none')
    is_active  = models.BooleanField(default=False)

    # objects       = models.Manager()
    objects    = UserManager()

    USERNAME_FIELD  = 'username'
    PASSWORD_FIELD  = 'password'
    REQUIRED_FIELDS = []


    @register.filter(name="getDate")
    def getDate(self):
        jdt.set_locale('fa_IR')
        jd    = jdt.date.fromgregorian(date=self.join_date).strftime('%d %B  %Y')
        ls    = jdt.datetime.fromgregorian(date=self.last_seen).strftime('%H:%M %Y %B %d')
        dates = {'jd': jd, 'ls': ls}
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
        print("get questions >>>>>>>>>>>>>>>>")
        print(self.username)
        try:
            questions = QuestionModel.objects.filter(author=self)
        except ObjectDoesNotExist:
            questions = None
        return questions



    @register.filter(name='getAnswers')
    def getAnswers(self):
        try:
            answers = AnswerModel.objects.filter(author=self)
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



