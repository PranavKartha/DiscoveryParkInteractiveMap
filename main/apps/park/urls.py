from django.conf.urls import url
from . import views

urlpatterns =[
	url(r'^$', views.index),
    url(r'^entermsg$', views.EnterResponse),
    url(r'^thankyou/', views.thankpage),
    # url(r'^pattern/', views.pattern_success)
]