"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView, DetailView, TemplateView, \
  CreateView
from repository.forms import SimpleSearch, AdvancedSearch
from repository.models import CorpusDescription
from settings import ITEMS_PER_PAGE
import logging

logger = logging.getLogger('cocos')

LOOKUP_FIELDS = ('name', 'location', 'coli_path', 'dfki_path', 'language',
  'description', 'comment', 'license_holder', 'contact')

ADVANCED_FIELDS = ('name', 'location', 'language', 'description',
  'comment', 'license_holder', 'contact')


class CorpusListView(ListView):
    """Return a generic view for listing the corpora in the database."""
    model = CorpusDescription
    context_object_name = 'corpus_list'
    paginate_by = ITEMS_PER_PAGE
    template_name = 'repository/list.html'


class CorpusByLocationView(CorpusListView):
    """Return a generic view for listing corpora according to their location"""
    template_name = 'repository/list_by_location.html'

    def get_queryset(self):
        """Return a queryset that is filtered by the corpus location."""
        return CorpusDescription.objects.filter(
          location__iexact=self.kwargs['location'])

    def get_context_data(self, **kwargs):
        """Extend the template context by variable 'location'."""
        context = super(CorpusByLocationView, self).get_context_data(**kwargs)
        context['location'] = self.kwargs['location']
        return context


class CorpusDetailView(DetailView):
    """Return a generic view for rendering the corpus details."""
    model = CorpusDescription
    context_object_name = 'corpus'
    template_name = 'repository/details.html'


class MainPageView(TemplateView):
    """Return a frontpage that links to browse and upload subpages."""
    template_name = 'repository/frontpage.html'


class UploadView(CreateView):
    """Render a form for submitting new corpus descriptions."""
    model = CorpusDescription
    success_url = '/'
    template_name = 'repository/upload.html'


def search(request):
    """Render the simple search view."""
    if request.method == 'POST':
        form = SimpleSearch(request.POST)

        if form.is_valid():
            keywords = form.cleaned_data['keywords']

            request.session['keywords'] = keywords.split()

            results = []
            if keywords:
                for keyword in keywords.split():
                    for field in LOOKUP_FIELDS:
                        partial_results = eval('CorpusDescription.' \
                          'objects.filter({0}__icontains="{1}")'
                          .format(field, keyword))

                        for corpus_description in partial_results:
                            if not corpus_description in results:
                                results.append(corpus_description)
    else:
        form = SimpleSearch()
        results = None

    dictionary = {'form':form, 'results':results}

    return render_to_response('repository/search.html',
      dictionary, context_instance=RequestContext(request))


def advanced_search(request):
    """Render the advanced search view."""
    if request.method == 'POST':
        form = AdvancedSearch(request.POST)

        if form.is_valid():
            results = []

            request.session['keywords'] = []

            for field in ADVANCED_FIELDS:
                field_results = []
                keywords = form.cleaned_data[field]

                request.session['keywords'].append(keywords.split())

                if keywords:
                    for keyword in keywords.split():
                        partial_results = eval('CorpusDescription.' \
                          'objects.filter({0}__icontains="{1}")'
                          .format(field, keyword))

                        for corpus_description in partial_results:
                            if not corpus_description in field_results:
                                field_results.append(corpus_description)

                    results.append(sorted(field_results))

            # We now build the global results list using outer Boolean AND.
            # Keywords for a specific field still use inner Boolean OR.
            check = lambda x: all(x in y for y in results)
            filtered_results = [y for x in results for y in x if check(y)]
            results = list(set(filtered_results))

    else:
        form = AdvancedSearch()
        results = None

    dictionary = {'form':form, 'results':results}

    return render_to_response('repository/search_advanced.html',
      dictionary, context_instance=RequestContext(request))


def log_user_in(request):
    """Log a user in."""
    error_message = ""
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                logger.info('User "{}" has logged in.'.format(username))
                return HttpResponseRedirect('/')
            else:
                error_message = 'not_active'
                logger.warning('User "{}" has logged in but is not active.'
                  .format(username))
        else:
            error_message = 'not_authenticated'
            logger.error('User "{}" tried to log in. '.format(username) +
              'Either the password is wrong or the user is not authenticated.')
    else:
        form = AuthenticationForm()

    return render_to_response('repository/login.html',
      {'form': form, 'error': error_message},
      context_instance=RequestContext(request))


def log_user_out(request):
    """Log a currently logged in user out."""
    logger.info('User "{}" has logged out.'.format(request.user))
    logout(request)
    return render_to_response('repository/frontpage.html',
      context_instance=RequestContext(request))