"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@gmail.com>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

import logging

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView, TemplateView

from cocos.repository.forms import SimpleSearch, AdvancedSearch, \
    CorpusDescriptionForm, FeedbackMessageForm
from cocos.repository.models import CorpusDescription
from cocos.settings import ITEMS_PER_PAGE

logger = logging.getLogger('cocos')

LOOKUP_FIELDS = ('name', 'location', 'coli_path', 'dfki_path', 'language',
  'description', 'comment', 'license_holder', 'contact')

ADVANCED_FIELDS = ('name', 'location', 'language', 'description',
  'comment', 'license_holder', 'contact')


# pylint: disable-msg=R0901
class CorpusListView(ListView):
    """Return a generic view for listing the corpora in the database."""
    model = CorpusDescription
    context_object_name = 'corpus_list'
    paginate_by = ITEMS_PER_PAGE
    template_name = 'repository/base_list.html'


# pylint: disable-msg=R0901,E1101
class CorpusByLocationView(CorpusListView):
    """Return a generic view for listing corpora according to their location"""
    template_name = 'repository/base_list-by-location.html'

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
    template_name = 'repository/base_details.html'


class MainPageView(TemplateView):
    """Return a frontpage that links to browse and upload subpages."""
    template_name = 'repository/base_frontpage.html'


def search(request):
    """Render the simple search view."""
    results = None
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

    dictionary = {'form':form, 'results':results}

    return render(request, 'repository/base_search.html', dictionary)


def advanced_search(request):
    """Render the advanced search view."""
    results = None
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

    dictionary = {'form':form, 'results':results}

    return render(request, 'repository/base_search-advanced.html', dictionary)


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

    dictionary = {'form': form, 'error': error_message}

    return render(request, 'repository/base_login.html', dictionary)


def log_user_out(request):
    """Log a currently logged in user out."""
    logger.info('User "{}" has logged out.'.format(request.user))
    logout(request)
    return render(request, 'repository/base_frontpage.html')


@login_required(login_url='/accounts/login')
def upload(request):
    """Render a form for submitting new corpus descriptions."""
    if request.method == 'POST':
        form = CorpusDescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            new_corpus = form.save(commit=False)
            new_corpus.contributor = request.user
            new_corpus.save()

            logger.info(
              'New corpus description uploaded by user "{}". Title: "{}".'
              .format(new_corpus.contributor, new_corpus.name.encode('utf-8')))

            messages.success(request,
              'Corpus description uploaded successfully! '
              'Just enter more if you want.')
        else:
            logger.warning(
              'User "{}" tried to upload a new corpus description but failed.'
              .format(request.user))

            messages.error(request,
              'Upload has failed! Please fill in all required slots.')
    else:
        form = CorpusDescriptionForm()

    dictionary = {'form': form}

    return render(request, 'repository/base_upload.html', dictionary)


@login_required(login_url='/accounts/login')
def feedback(request):
    """Render a form for submitting new feedback messages."""
    if request.method == 'POST':
        form = FeedbackMessageForm(request.POST, request.FILES)
        if form.is_valid():
            new_feedback = form.save(commit=False)
            new_feedback.user = request.user
            # The status of a new message is set to 'Open' by default
            new_feedback.status = 'O'
            new_feedback.save()

            logger.info(
              'New feedback message uploaded by user "{}". Subject: "{}".'
              .format(new_feedback.user, new_feedback.subject.encode('utf-8')))

            messages.success(request,
              'Thanks for your feedback! We will deal with it soon.')
        else:
            logger.warning(
              'User "{}" tried to send a feedback message but failed.'
              .format(request.user))

            messages.error(request,
              'Feedback submission has failed! '
              'Please fill in all required slots.')
    else:
        form = FeedbackMessageForm

    dictionary = {'form': form}

    return render(request, 'repository/base_feedback.html', dictionary)