from django.conf import settings
from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.STATIC_ROOT }),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT }),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/', include('registration.backends.default.urls')),
    url(r'^$', 'profiles.views.all', name='home'),
    url(r'^members/(?P<username>\w+)/find/Job', 'profiles.views.job', name='job'),
    url(r'^members/(?P<username>\w+)/find/Message', 'profiles.views.message', name='message'),
    url(r'^members/(?P<username>\w+)/find/Search', 'profiles.views.search', name='search'),
    url(r'^members/(?P<username>\w+)/find/Call', 'profiles.views.call', name='call'),
    url(r'^members/(?P<username>\w+)/find', 'profiles.views.find', name='find'),
    url(r'^members/(?P<username>\w+)/$', 'profiles.views.single_user', name='profile'),
    url(r'^edit/$', 'profiles.views.edit_profile', name='edit_profile'),
    (r'^edit/jobs$', 'profiles.views.edit_jobs'),
    (r'^edit/locations$', 'profiles.views.edit_locations'),
    url(r'^questions/$', 'questions.views.all_questions', name='questions'),
)




