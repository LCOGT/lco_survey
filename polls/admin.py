#-*- coding: utf-8 -*-
from django.contrib import admin

from .models import Choice, Question, Survey, LIKERT_CHOICES, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ['survey','date']
    list_filter = ['survey',]


class ChoiceInline(admin.TabularInline):
    model = Choice
    readonly_fields = ('votes',)
    extra = 0

def reset_votes(modeladmin, request, queryset):
    queryset.update(votes=0)
reset_votes.short_description = "Reset choice votes"

class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice','votes','question','survey']
    actions = [reset_votes]

def add_choices(modeladmin, request, queryset):
    for s in queryset:
        for q in Question.objects.all():
            for l in LIKERT_CHOICES:
                c = Choice()
                c.question = q
                c.survey = s
                c.choice = l[0]
                c.save()
add_choices.short_description = "Add choices to selected survey questions"

class SurveyAdmin(admin.ModelAdmin):
    inlines = [ChoiceInline]
    actions = [add_choices]
    list_display = ['name', 'active','startdate','enddate']
    list_filter = ['active',]

admin.site.register(Question)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Survey, SurveyAdmin)
admin.site.register(Comment, CommentAdmin)
