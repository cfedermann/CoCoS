"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@gmail.com>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

import os
import sys

from datetime import datetime
from django.core.management import setup_environ

def usage():
    """Prints usage instructions to screen."""
    print "\nUsage: python export_data.py {xml|json}\n"


def export_data(filetype):
    """
    Export the data currently being in the database
    and save it in folder 'exported_data'.
    """
    from django.core import serializers
    
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
    
    # Properly set DJANGO_SETTINGS_MODULE environment variable.
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    PROJECT_HOME = os.path.normpath(os.getcwd() + "/..")
    sys.path.append(PROJECT_HOME)
    
    # We have just added cocos to the system path list, hence this works.
    from cocos import settings
    from cocos.repository.models import CorpusDescription, FeedbackMessage
    
    # Setup Django environment using settings module.
    setup_environ(settings)
    
    # Export data using export_data() method.
    export_data(sys.argv[1])
