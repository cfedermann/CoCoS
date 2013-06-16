"""
Project: Corpora Collection System (CoCoS)
Authors: Christian Federmann <cfedermann@gmail.com>,
         Peter Stahl <pstahl@coli.uni-saarland.de>
"""

import os
import sys

def usage():
    """Prints usage instructions to screen."""
    print "\nUsage: python import_data.py <filename.{xml|json}>\n"


def import_data(filename):
    """Import the current dump back into the database."""
    from django.core import serializers
    
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
    
    # Properly set DJANGO_SETTINGS_MODULE environment variable.
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
    PROJECT_HOME = os.path.normpath(os.getcwd() + "/..")
    sys.path.append(PROJECT_HOME)
    
    # Import data using import_data() method.
    import_data(sys.argv[1])
