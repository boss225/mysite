# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible #fix unicode

# Create your models here.
@python_2_unicode_compatible
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()
 
    def __str__(self): 
        return self.name