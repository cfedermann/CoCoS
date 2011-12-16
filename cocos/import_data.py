"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@dfki.de>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""
import settings
import sys
from django.core import serializers
from django.core.management import setup_environ

setup_environ(settings)

def usage():
    """Prints usage instructions to screen."""
    print "\nUsage: python import_data.py <data.{xml|json}>\n"


def import_data(filename):
    """Import the current dump back into the database."""

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

    print "\tModel data successfully written to database"


if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(-1)

    import_data(sys.argv[1])