# -*- coding: utf-8 -*-
from __future__ import unicode_literals


from django.contrib import admin

# Register your models here.
from .models import Question, Choice

class ChoiceInLine(admin.TabularInline):
    model = Choice 
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInLine]
    list_display = ('question_text','pub_date')
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)