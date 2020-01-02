#-*- coding: utf-8 -*-
from datetime import datetime

from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.contrib import messages

from .models import Choice, Question, Survey, LIKERT_CHOICES, LIKERT_ICONS, Comment

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'survey_list'

    def get_queryset(self):
        return Survey.objects.all()

class ThanksView(generic.DetailView):
    slug_url_kwarg = 'id'
    slug_field = 'id'
    model = Survey
    template_name = 'polls/thanks.html'

class DetailView(generic.DetailView):
    slug_url_kwarg = 'id'
    slug_field = 'id'
    model = Survey
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the questions
        context['questions'] = question_list(self.object)
        cookie = self.request.COOKIES.get(self.object.cookie_name, None)
        if cookie and cookie == str(self.object.id):
            context['answered'] = True
        return context

class ResultsView(LoginRequiredMixin, generic.DetailView):
    slug_url_kwarg = 'id'
    slug_field = 'id'
    model = Survey
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['answers'] = question_list(self.object)
        context['comments'] = Comment.objects.filter(survey=self.object)
        return context

def question_list(survey):
    questions = Question.objects.filter(survey=survey).distinct()
    qs = []

    for q in questions:
        tmp_q = {}
        tmp_q['id'] = q.id
        tmp_q['text'] = q.text
        choices = Choice.objects.filter(question=q.id,survey=survey).order_by('choice')
        ch_tmp = []
        for ch in choices:
            ch_tmp.append({'text' : ch.get_choice_display(), 'id':ch.id,'icon':LIKERT_ICONS[ch.choice],'votes':ch.votes})
        tmp_q['choices'] = ch_tmp
        qs.append(tmp_q)
    return qs

def vote(request, id):
    error = None
    good_choices = []
    s = get_object_or_404(Survey, pk=id)
    question_ids = s.answer.all().distinct().values_list('id', flat=True)
    field_names = ['question-{}'.format(i) for i in question_ids]
    for field_id in field_names:
        choice_id = request.POST.get(field_id,'999')
        try:
            selected_choice = s.choice_set.get(pk=choice_id)
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the poll voting form.
            error = "Please select answers for all questions"
        else:
            good_choices.append(selected_choice)

    if error:
        messages.error(request,error)
        return HttpResponseRedirect(reverse('polls:detail', args=(s.id,)))
    else:
        for ch in good_choices:
            ch.votes += 1
            ch.save()

    if request.POST.get('comment',None):
        newcomment = Comment(text=request.POST.get('comment'), date=datetime.utcnow(),survey=s)
        newcomment.save()

    response = HttpResponseRedirect(reverse('polls:thanks', args=(s.id,)))
    if not request.COOKIES.get(s.cookie_name, None):
        response.set_cookie(s.cookie_name, s.id, max_age=31536000)

    return response
