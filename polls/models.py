#-*- coding: utf-8 -*-
from django.db import models
import uuid

LIKERT_CHOICES = (
                ('A','Agree'),
                ('D','Disagree'),
                ('N','Neither Agree Nor Disagree')
                )

class Question(models.Model):
    text = models.CharField(max_length=200)

    def __str__(self):
        return self.text

class Survey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(default='', max_length=20)
    active = models.BooleanField(default=False)
    startdate = models.DateTimeField()
    enddate = models.DateTimeField()
    answer = models.ManyToManyField(Question, through="Choice")
    cookie_name = models.CharField(max_length=20, help_text="Should start 'lco_fb_'")

    def __str__(self):
        return "{} {} - {}".format(self.name, self.startdate.strftime("%Y-%m-%d"), self.enddate.strftime("%Y-%m-%d"))

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=2, choices=LIKERT_CHOICES)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.get_choice_text_display()
