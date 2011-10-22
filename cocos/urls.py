"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

from django.conf.urls.defaults import include, patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from repository.views import CorpusListView, CorpusByLocationView, \
  CorpusDetailView, MainPageView, UploadView

admin.autodiscover()

urlpatterns = patterns('repository.views',

    url(r'^$', MainPageView.as_view(), name='cocos-frontpage'),
    url(r'^browse/page=(?P<page>[0-9]+)/$', CorpusListView.as_view(),
      name='corpus-list'),
    url(r'^browse/\$(?P<pk>\d+)/$', CorpusDetailView.as_view(),
      name='corpus-details'),
    url(r'^browse/(?P<location>coli|dfki)/page=(?P<page>[0-9]+)/$',
      CorpusByLocationView.as_view(), name='corpus-list-by-location'),
    #url(r'^upload/$', UploadView.as_view(), name='upload-form'),
    url(r'^search/$', 'search', name='search'),
    url(r'^advanced/$', 'advanced_search', name='advanced'),

    url(r'^accounts/login/$', 'log_user_in', name='login-form'),
    url(r'^accounts/logout/$', 'log_user_out', name='logout'),

    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('repository.views_deprecated',

    #url(r'^$', 'frontpage', name='cocos-frontpage'),
    #url(r'^browse/page=(?P<page>[0-9]+)/$', 'corpus_list', name='corpus-list'),
    #url(r'^browse/\$(?P<corpus_id>\d+)/$', 'corpus_details',
    #  name='corpus-details'),
    #url(r'^browse/(?P<location>coli|dfki)/page=(?P<page>[0-9]+)/$',
    #  'corpus_by_location', name='corpus-list-by-location'),
    url(r'^upload/$', 'upload', name='upload-form'),

)

#urlpatterns += patterns('django.contrib.auth.views',

    #url(r'^accounts/login/$', 'login',
    #  {'template_name': 'repository/cocos_login.html'}, name='login-form'),
    #url(r'^accounts/logout/$', 'logout',
    #  {'template_name': 'repository/cocos_logout.html'}, name='logout'),
#)

urlpatterns += staticfiles_urlpatterns()