# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class msgcode(models.Model):
	phone = models.CharField(max_length = 11, primary_key = True)
	time = models.DateTimeField(auto_now = True)
	code = models.CharField(max_length = 6)
	