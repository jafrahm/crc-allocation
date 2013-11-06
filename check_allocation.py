#!/usr/bin/env python

print "Requesting data, this may take up to 30 seconds..."

import sys
import getpass
from pprint import pprint

import urllib2

try:
    import json
except:
    print "json not found plese try use EPD to make sure you are using the correct distribution"
    sys.exit(1)
try:
    import argparse
except:
    print "argparse couldn't be found, this script requires python>2.7"
    sys.exit(1)


def setup_options():
    desc="""Research computing maintained script to help users check their
allocation balances from the command line"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument("-l",help="List members of the allocations",
                       action="store_true")
    return parser.parse_args()

def get_allocations():
    req=urllib2.Request("https://portals.rc.colorado.edu/reporting/api/projects/rcops/json/")

    f=urllib2.urlopen(req)
    response=json.loads(f.read())
    f.close()
    return response

if __name__=="__main__":
    
    args=setup_options()
    username=getpass.getuser()

    response=get_allocations()

    if username=='rcops':
       print "Username rcops shouldn't belong to any groups, using jabr9336 instead"
       username='jabr9336'

    print "You are listed as being a member of the following projects"
    template="{0:40} | {1:20} | {2:10.0f} | {3:10.0f} | {4:10.0f} | {5:10}"
    htemplate="{0:40} | {1:20} | {2:10} | {3:10} | {4:10} | {5:10}"
    print htemplate.format("Title","Name","Balance","Used","Available","End Date")
    for project in response:
       members = [x['username'] for x in project['members']]
       if username in members:
          print template.format(project['title'][:39],project['name'],project['credit'],project['used'],project['balance'],project['end_date'].split('T')[0])
          if args.l: 
             print "  Memberlist:"
             for user in members:
                print "\t%s"%user
