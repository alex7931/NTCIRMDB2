#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .forms import *
from hashlib import sha512
from uuid import  uuid4
import time
import datetime
from mongoengine import *
# Create your models here.
user_group_list = (
    ('admin', u'admin'),
    ('normal_user', u'user'),
)


class TimestampGenerator(object):

    def __init__(self, seconds=0):
        self.seconds = seconds

    def __call__(self):
        return int(time.time()) + self.seconds


class KeyGenerator(object):

    def __init__(self, length):
        self.length = length

    def __call__(self):
        key = sha512(uuid4().hex).hexdigest()[0:self.length]
        return key

class User(Document):
    username = StringField(unique=True, required=True)
    password = StringField(required=True)
    email = EmailField(required=True)
    # sex = StringField(choices=sex_choices)
    name = StringField(required=True)
    age = IntField(required=True)
    # search_frequency = StringField(required=True, choices=search_frequency_choices)

    user_groups = ListField(StringField(choices=user_group_list), default=['normal_user'])
    signup_time = DateTimeField(default=datetime.datetime.now)
    last_login = DateTimeField(default=datetime.datetime.now)
    login_num = IntField(default=0)


class ResetPasswordRequest(Document):
    user = ReferenceField(User)
    token = StringField(default=KeyGenerator(12))
    expire = IntField(default=TimestampGenerator(60*60*30))







