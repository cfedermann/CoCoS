"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

import os
import settings
import sys

from django.core import serializers
from django.core.management import setup_environ
setup_environ(settings)

from repository.models import CorpusDescription, FeedbackMessage

def usage():
    """Prints usage instructions to screen."""
    print "\nUsage: python export_data.py <filename.{xml|json}>\n"


def export_data(filename):
    """
    Export the data currently being in the database
    and save it in folder 'exported_data'.
    """
    if filename.endswith("xml"):
        serializer = serializers.get_serializer("xml")
    elif filename.endswith("json"):
        serializer = serializers.get_serializer("json")
    else:
        raise RuntimeError("File name must be of extension 'xml' or 'json'!")

    if not os.path.isdir("exported_data"):
        os.mkdir("exported_data")
    output = open("exported_data/" + filename, "w")

    new_serializer = serializer()
    all_objects = list(CorpusDescription.objects.all()) + \
      list(FeedbackMessage.objects.all())
    new_serializer.serialize(all_objects, stream=output)
    output.close()

    print "\tModel data successfully written to", filename


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(-1)

    export_data(sys.argv[1])