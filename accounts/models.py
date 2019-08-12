from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser, UserManager as BaseUserManager
from beauty.models import Cosmetic
import datetime

today = datetime.datetime.now()

class UserManager(BaseUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(gender=self.model.GENDER_OTHER, nickname="", birth="", *args, **kwargs)

class User(AbstractUser):
    GENDER_MALE = 'm'
    GENDER_FEMALE = 'f'
    GENDER_OTHER = 'o'
    CHOICES_GENDER = (
        (GENDER_MALE, '남성'),
        (GENDER_FEMALE, '여성'),
        (GENDER_OTHER, '기타'),
    )
    gender = models.CharField(max_length=1, choices=CHOICES_GENDER)
    nickname = models.CharField(max_length=50)
    birth = models.DateField(auto_now=False, auto_now_add=False, default=today)
    cosmetic = models.ManyToManyField(Cosmetic)

    def __str__(self):
        return self.username