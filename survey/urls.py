from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.claim_list, name='claim_list'),
	url(r'^claim/(?P<pk>\d+)/$', views.claim_detail, name='claim_detail'),
    url(r'^claim/new/$', views.claim_new, name='claim_new'),
]