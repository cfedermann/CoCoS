"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

from django.contrib.auth.models import User
from django.db import models

MODEL_VERSION = 1

LANGUAGES = (
      ('CN', 'Chinese'),
      ('DE', 'German'),
      ('EN', 'English'),
      ('ES', 'Spanish'),
      ('FR', 'French'),
      ('IT', 'Italian'),
      ('ML', 'Multilingual')
    )

LOCATIONS = (
      ('DFKI', 'DFKI'),
      ('COLI', 'CoLi'),
    )

class CorpusDescription(models.Model):
    """The corpus description model.

    This model provides the following fields:
    Mandatory fields: Name, Location, Language, Annotation.
    Optional fields: Description, Comment, License holder, Contact.
    """

    # Mandatory fields
    name = models.CharField(max_length=50,
      help_text="The name of the corpus, e.g. <i>American National Corpus</i>.")
    #url = models.URLField(help_text="The URL to the corpus website, e.g. \
    #  <i>http://americannationalcorpus.org/</i>")
    location = models.CharField(choices=LOCATIONS, max_length=4,
      help_text="Which server(s) is the corpus located on?")
    coli_path = models.CharField(blank=True, max_length=100,
      help_text="The path to the corpus on the CoLi server",
      verbose_name="Path on CoLi server")
    dfki_path = models.CharField(blank=True, max_length=100,
      help_text="The path to the corpus on the DFKI server",
      verbose_name="Path on DFKI server")
    language = models.CharField(choices=LANGUAGES, max_length=2,
      help_text="Which language does the corpus provide its data in?")
    annotation = models.BooleanField(help_text="Is the corpus annotated?")

    # Optional fields
    description = models.TextField(blank=True,
      help_text="A short description of the corpus' content")
    comment = models.TextField(blank=True,
      help_text="Some further comments or remarks")
    license_holder = models.CharField(blank=True, max_length=100,
      help_text="Who is the license holder of this corpus?")
    contact = models.EmailField(blank=True,
      help_text="The license holder's email address")
    file = models.FileField(upload_to="files/%Y/%m/%d", blank=True)

    # The user who uploaded the current corpus description
    uploader = models.ForeignKey(User, related_name='+')

    # Timestamp dates for the admin backend
    date_of_first_creation = models.DateTimeField(auto_now_add=True,
      help_text="Timestamp for adding the corpus to the database",
      verbose_name="date of first creation")

    date_of_last_modification = models.DateTimeField(auto_now=True,
      help_text="Timestamp for the last modification",
      verbose_name="date of last modification")



    def __unicode__(self):
        return self.name