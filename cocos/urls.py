"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

from django.conf.urls.defaults import include, patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from cocos.repository.views import CorpusListView, CorpusByLocationView, \
  CorpusDetailView, MainPageView

admin.autodiscover()

# pylint: disable-msg=E1120
urlpatterns = patterns('repository.views',

    url(r'^$', MainPageView.as_view(), name='cocos-frontpage'),
    url(r'^browse/page=(?P<page>[0-9]+)/$', CorpusListView.as_view(),
      name='corpus-list'),
    url(r'^browse/corpus_id=(?P<pk>\d+)/$', CorpusDetailView.as_view(),
      name='corpus-details'),
    url(r'^browse/(?P<location>coli|dfki)/page=(?P<page>[0-9]+)/$',
      CorpusByLocationView.as_view(), name='corpus-list-by-location'),

    url(r'^upload/$', 'upload', name='upload-form'),
    url(r'^feedback/$', 'feedback', name='feedback-form'),

    url(r'^search/$', 'search', name='search'),
    url(r'^advanced/$', 'advanced_search', name='advanced'),

    url(r'^accounts/login/$', 'log_user_in', name='login-form'),
    url(r'^accounts/logout/$', 'log_user_out', name='logout'),

    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()