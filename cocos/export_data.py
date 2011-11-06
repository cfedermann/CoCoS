"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

import os
import sys
import settings
from django.core import serializers
from django.core.management import setup_environ
from repository.models import CorpusDescription, FeedbackMessage

setup_environ(settings)

def export_data(datatype, filename):
    """
    Export the data currently being in the database
    and save it in folder 'exported_data'.
    """
    if not os.path.isdir("exported_data"):
        os.mkdir("exported_data")
    output = open("exported_data/" + filename, "w")
    serializer = serializers.get_serializer(datatype)
    new_serializer = serializer()
    all_objects = list(CorpusDescription.objects.all()) + \
      list(FeedbackMessage.objects.all())
    new_serializer.serialize(all_objects, stream=output)
    output.close()

    print "Model data successfully written to", filename


if __name__ == "__main__":
    # Exporting the DJANGO_SETTINGS_MODULE does not work here
    export_data(sys.argv[1], sys.argv[2])