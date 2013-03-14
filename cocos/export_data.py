"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

import os
import sys

from datetime import datetime
from django.core import serializers
from django.core.management import setup_environ

# pylint: disable-msg=W0403
import settings

from repository.models import CorpusDescription, FeedbackMessage

setup_environ(settings)

def usage():
    """Prints usage instructions to screen."""
    print "\nUsage: python export_data.py {xml|json}\n"


def export_data(filetype):
    """
    Export the data currently being in the database
    and save it in folder 'exported_data'.
    """
    if filetype == "xml":
        serializer = serializers.get_serializer("xml")
    elif filetype == "json":
        serializer = serializers.get_serializer("json")
    else:
        raise RuntimeError("Extension must be either 'xml' or 'json'!")

    if not os.path.isdir("exported_data"):
        os.mkdir("exported_data")

    dump_file = "cocos_dump_" + str(datetime.today()).replace(" ", "_") + "." + filetype
    output = open("exported_data/" + dump_file, "w")

    new_serializer = serializer()
    all_objects = list(CorpusDescription.objects.all()) + \
      list(FeedbackMessage.objects.all())
    new_serializer.serialize(all_objects, stream=output)
    output.close()

    print "\tModel data successfully written to", dump_file


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(-1)

    export_data(sys.argv[1])
