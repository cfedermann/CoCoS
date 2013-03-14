"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

import os
import sys

from django.core import serializers
from django.core.management import setup_environ

# pylint: disable-msg=W0403
import settings

setup_environ(settings)

def usage():
    """Prints usage instructions to screen."""
    print "\nUsage: python import_data.py <filename.{xml|json}>\n"


def import_data(filename):
    """Import the current dump back into the database."""

    if os.path.isfile(os.getcwd() + "/exported_data/" + filename):
        if filename.endswith("xml"):
            data = open("exported_data/" + filename, "r")
            for deserialized_object in serializers.deserialize("xml", data):
                deserialized_object.save()
            data.close()

        elif filename.endswith("json"):
            data = open("exported_data/" + filename, "r")
            for deserialized_object in serializers.deserialize("json", data):
                deserialized_object.save()
            data.close()

        else:
            raise RuntimeError("File name must be of extension 'xml' or 'json'!")

    else:
        raise IOError("The file " + filename + " was not found!")

    print "\tModel data taken from", filename, "successfully written to database"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(-1)

    import_data(sys.argv[1])
