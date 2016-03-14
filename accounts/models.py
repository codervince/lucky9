#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class UserProfile(models.Model):
    LANGUAGES =(
    ('en_US', 'English'),
    ('zh_HK', '中文'),
    ('zh_CN', '官话'),
    ('de_DE', 'Deutsch'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # user = models.OneToOneField(User)
    joined = models.DateTimeField(auto_now_add=True)
    language = models.CharField(max_length=10, choices=LANGUAGES) #iso code

    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
