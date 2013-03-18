"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@gmail.com>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

from django import forms

from cocos.repository.models import CorpusDescription, FeedbackMessage, \
  LOCATIONS, LANGUAGES

LOCATIONS_AND_EMPTY = [('', '---------')] + LOCATIONS
LANGUAGES_AND_EMPTY = [('', '---------')] + LANGUAGES

# pylint: disable-msg=R0924
class CorpusDescriptionForm(forms.ModelForm):
    """A ModelForm for the corpus description model."""
    
    class Meta:
        """
        A meta class for specifying which model this ModelForm is built upon.
        """
        model = CorpusDescription
        fields = ('name', 'location', 'language', 'annotation', 'coli_path',
          'dfki_path', 'license_holder', 'contact', 'description', 'comment',
          'sample_file')
        #exclude = ('contributor',)


# pylint: disable-msg=R0924
class FeedbackMessageForm(forms.ModelForm):

    class Meta:
        model = FeedbackMessage
        exclude = ('user', 'status')


# pylint: disable-msg=R0924
class SimpleSearch(forms.Form):
    """Render a single text input."""
    keywords = forms.CharField(max_length=200, required=False)


# pylint: disable-msg=R0924
class AdvancedSearch(forms.Form):
    """Render a complex search form for different model fields."""
    name = forms.CharField(max_length=200, required=False, label="Name")
    location = forms.ChoiceField(choices=LOCATIONS_AND_EMPTY, required=False, label="Location")
    language = forms.ChoiceField(choices=LANGUAGES_AND_EMPTY, required=False, label="Language")
    description = forms.CharField(max_length=200, required=False, 
      label="Description")
    comment = forms.CharField(max_length=200, required=False, label="Comment")
    license_holder = forms.CharField(max_length=200, required=False, 
      label="License Holder")
    contact = forms.CharField(max_length=200, required=False, label="Contact")
    