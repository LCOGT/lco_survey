#-*- coding: utf-8 -*-
from django.contrib import admin

from .models import Choice, Question, Survey


class ChoiceInline(admin.TabularInline):
    model = Choice
    readonly_fields = ('votes',)
    extra = 0

class SurveyAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]


admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Survey, SurveyAdmin)
