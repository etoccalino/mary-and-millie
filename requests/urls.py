from django.conf.urls import patterns, url
import views

urlpatterns = patterns('',
    url(r'^$', views.requests, name="requests"),
    url(r'^new/$', views.new_request, name="new_request"),
    url(r'^(?P<request_pk>\w+)/$', views.request, name="request"),
)
