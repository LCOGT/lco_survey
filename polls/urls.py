#-*- coding: utf-8 -*-
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings

from . import views

app_name = "polls"
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<uuid:id>/', views.DetailView.as_view(), name='detail'),
    path('<uuid:id>/thanks/', views.ThanksView.as_view(), name='thanks'),
    path('<uuid:id>/results/', views.ResultsView.as_view(), name='results'),
    path('<uuid:id>/vote/', views.vote, name='vote'),
]  + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
