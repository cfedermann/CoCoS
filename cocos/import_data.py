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

def import_data(datatype, filename):
    """Import the current dump back into the database."""
    data = open("exported_data/" + filename, "r")
    for deserialized_object in serializers.deserialize(datatype, data):
        deserialized_object.save()
    data.close()

    print "Model data succesfully written to database"


if __name__ == "__main__":
    import_data(sys.argv[1], sys.argv[2])