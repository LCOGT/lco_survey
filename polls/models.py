#-*- coding: utf-8 -*-
from django.db import models
import uuid

LIKERT_CHOICES = (
                (1,'Agree'),
                (2,'Neither Agree Nor Disagree'),
                (3,'Disagree'),
                )

LIKERT_ICONS = {1:'polls/img/agree.png',2:'polls/img/neither.png',3:'polls/img/disagree.png'}


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
    choice = models.PositiveSmallIntegerField(default=2, choices=LIKERT_CHOICES)
    votes = models.IntegerField(default=0)

    def icon(self):
        return LIKERT_ICONS[self.choice]

    def __str__(self):
        return self.get_choice_display()

    class Meta:
        unique_together = ['question','survey','choice']

class Comment(models.Model):
    text = models.TextField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return "Comment for {} on {}".format(self.survey, self.date)
