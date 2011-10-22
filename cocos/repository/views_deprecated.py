"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import list_detail
from repository.forms import CorpusDescriptionForm
from repository.models import CorpusDescription
from settings import ITEMS_PER_PAGE
import logging

logger = logging.getLogger('cocos')

LOOKUP_FIELDS = ('name', 'location', 'coli_path', 'dfki_path', 'language',
  'description', 'comment', 'license_holder', 'contact')

ADVANCED_FIELDS = ('name', 'location', 'language', 'description',
  'comment', 'license_holder', 'contact')

def frontpage(request):
    """Return a frontpage that links to browse and upload subpages."""
    return render_to_response('repository/frontpage.html')

def corpus_list(request, page):
    """Return a generic view for listing the corpora in the database."""
    return list_detail.object_list(
      request,
      page=page,
      queryset=CorpusDescription.objects.all(),
      template_name='repository/list.html',
      template_object_name='corpus',
      paginate_by=ITEMS_PER_PAGE
    )

def corpus_details(request, corpus_id):
    """Return a generic view for rendering the corpus details."""
    return list_detail.object_detail(
      request,
      object_id=corpus_id,
      queryset=CorpusDescription.objects.all(),
      template_name='repository/cocos_details.html',
      template_object_name='corpus'
    )

def corpus_by_location(request, location, page):
    """Return a generic view for listing corpora according to their location"""
    return list_detail.object_list(
      request,
      page=page,
      queryset=CorpusDescription.objects.filter(location__iexact=location),
      template_name='repository/list_by_location.html',
      template_object_name='corpus',
      paginate_by=ITEMS_PER_PAGE,
      extra_context={"location":location}
    )


@login_required(login_url='/accounts/login')
def upload(request):
    """Render a form for submitting new corpus descriptions."""
    if request.method == 'POST':
        form = CorpusDescriptionForm(request.POST, request.FILES)
        if form.is_valid():
            new_corpus = form.save(commit=False)
            new_corpus.uploader = request.user
            new_corpus.save()

            logger.info(
              'New corpus description uploaded by user "{}". Title: "{}".'
              .format(new_corpus.uploader, new_corpus.name))

            return HttpResponseRedirect('/')
        else:
            logger.warning(
              'User "{}" tried to upload a new corpus description but failed.'
              .format(request.user))

            messages.error(request,
              'Upload has failed. Please fill in all required slots.')
    else:
        form = CorpusDescriptionForm()

    return render_to_response('repository/upload.html',
      {'form': form}, context_instance=RequestContext(request))