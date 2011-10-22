"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

from django import forms
from repository.models import CorpusDescription

class CorpusDescriptionForm(forms.ModelForm):
    """A ModelForm for the corpus description model."""
    
    class Meta:
        """
        A meta class for specifying which model this ModelForm is built upon.
        """
        model = CorpusDescription
        exclude = ('uploader',)
        
class SimpleSearch(forms.Form):
    """Render a single text input."""
    keywords = forms.CharField(max_length=200, required=False)
    
class AdvancedSearch(forms.Form):
    """Render a complex search form for different model fields."""
    name = forms.CharField(max_length=200, required=False, label="Name")
    location = forms.CharField(max_length=200, required=False, label="Location")
    language = forms.CharField(max_length=200, required=False, label="Language")
    description = forms.CharField(max_length=200, required=False, 
      label="Description")
    comment = forms.CharField(max_length=200, required=False, label="Comment")
    license_holder = forms.CharField(max_length=200, required=False, 
      label="License Holder")
    contact = forms.CharField(max_length=200, required=False, label="Contact")
    