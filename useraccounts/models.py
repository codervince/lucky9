#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import get_language_info
from django.utils.translation import ugettext_lazy as _
en_en = get_language_info('en')['name_local']
de_de = get_language_info('de')['name_local']
zh_cn = get_language_info('zh-hans')['name_local']
zh_tw = get_language_info('zh-hant')['name_local']
    # ('zh_HK', '中文'),
    # ('zh_CN', '官话'),

class UserProfile(models.Model):
    LANGUAGES =(
    ('en-us', en_en),
    ('zh-cn', zh_cn ),
    ('zh-tw', zh_tw ),
    ('de-de', de_de),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name=_('profile'),)
    # user = models.OneToOneField(User)
    joined = models.DateTimeField(auto_now_add=True)
    language = models.CharField(_('language'), max_length=10, choices=LANGUAGES, default='en-us') #iso code
    def __str__(self):
        return 'Profile for user {}'.format(self.user.username)
