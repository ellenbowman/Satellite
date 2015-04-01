from optparse import OptionParser
import os
import sys

manage_template = """#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%(application_home_dir)s.settings.%(environment)s")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
"""

wsgi_template = """ # -*- mode: python -*-
# vi: set ft=python :

import os
%(newrelic_import)s
%(newrelic_initialize)s

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%(application_home_dir)s.settings.%(environment)s")

# This application object is used by any WSGI server configured to use this
# file. This includes Django's development server, if the WSGI_APPLICATION
# setting points here.
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
%(newrelic_wrapper)s

# Apply WSGI middleware here.
# from helloworld.wsgi import HelloWorldApplication
# application = HelloWorldApplication(application)
"""


current_directory = os.path.dirname(os.path.abspath(__file__))

def create_manage_script(environment, application_home_dir):

    print 'creating manage script!!!!!!!!!!!!!!!!!!!'


    current_directory = os.path.dirname(os.path.abspath(__file__))
    outfile = os.path.join(current_directory, "manage.py")
    output = manage_template % {'environment': environment, 'application_home_dir': application_home_dir}
    try:
        with open(outfile, 'w') as management_file:
            management_file.write(output)
            print("manage.py written to %s" % outfile)
    except IOError:
        print("Can't write to %s" % outfile)


def create_wsgi(environment, application_home_dir):
    replacement_dict = {'environment': environment,
                        'newrelic_import': "",
                        'newrelic_initialize': "",
                        'newrelic_wrapper': "",
                        'application_home_dir': application_home_dir}


    outfile = os.path.join(current_directory, application_home_dir, "wsgi.py")
    output = wsgi_template % replacement_dict
    try:
        with open(outfile, 'w') as wsgifile:
            wsgifile.write(output)
            print("wsgi.py written to %s" % outfile)
    except IOError:
        print("Can't write to %s" % outfile)
        

if __name__ == "__main__":
    parser = OptionParser()
    (options, args) = parser.parse_args()
    environment = args[0]
    application_home_dir = "satellite_project"
    for fn in (create_manage_script, create_wsgi):
        fn(environment=environment, application_home_dir=application_home_dir)
