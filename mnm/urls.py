from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^requests/', include('requests.urls')),
    url(r'^socket\.io', 'requests.views.socketio'),
)
