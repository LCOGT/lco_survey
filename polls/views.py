#-*- coding: utf-8 -*-
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Choice, Question, Survey, LIKERT_CHOICES


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'active_survey_list'

    def get_queryset(self):
        return Survey.objects.all()


class DetailView(generic.DetailView):
    slug_url_kwarg = 'id'
    slug_field = 'id'
    model = Survey
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        questions = self.object.choice_set.all().values('id','question_id','question__text','choice_text','choice_text')
        qs = []
        choices = dict(LIKERT_CHOICES)
        for q in questions:
            tmp_q = q
            tmp_q['choice'] = choices[q['choice_text']]
            qs.append(tmp_q)
        context['questions'] = qs
        cookie = self.request.COOKIES.get(self.object.cookie_name, None)
        if cookie and cookie == str(self.object.id):
            context['answered'] = True
        return context

class ResultsView(generic.DetailView):
    slug_url_kwarg = 'id'
    slug_field = 'id'
    model = Survey
    template_name = 'polls/results.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['answers'] = self.object.choice_set.all().values('question_id','question__text','choice_text','id','votes')
        return context

def vote(request, id):
    error = None
    good_choices = []
    s = get_object_or_404(Survey, pk=id)
    question_ids = s.answer.all().distinct().values_list('id', flat=True)
    field_names = ['question-{}'.format(i) for i in question_ids]
    for field_id in field_names:
        choice_id = request.POST[field_id]
        try:
            selected_choice = s.choice_set.get(pk=choice_id)
        except (KeyError, Choice.DoesNotExist):
            # Redisplay the poll voting form.
            error = {
                'poll': s,
                'error_message': "You didn't select a choice.",
            }
        else:
            good_choices.append(selected_choice)
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
    if error:
        return render(request, 'polls/detail.html', error)
    else:
        for ch in good_choices:
            ch.votes += 1
            ch.save()

    response = HttpResponseRedirect(reverse('polls:results', args=(s.id,)))
    if not request.COOKIES.get(s.cookie_name, None):
        response.set_cookie(s.cookie_name, s.id, max_age=31536000)

    return response
