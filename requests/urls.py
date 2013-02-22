from django.conf.urls import patterns, include, url
import views

urlpatterns = patterns('',
    url(r'^new/$', views.new_request, name="new_request"),
)
