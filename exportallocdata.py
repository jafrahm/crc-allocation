#!/usr/bin/env python
import optparse
import urllib2
import json
import sys
import datetime


REQUEST_URL = 'https://portals.rc.colorado.edu/reporting/api/projects/%s/json/'


def print_single_project(project):
    values = []
    values.append(project['title'][:75])
    values.append(project['owner']['username'])
    values.append(project['name'])
    values.append(project['start_date'][:10])
    values.append(project['end_date'][:10])
    if project['over_limit']:
        values.append('over_limit')
    else:
        values.append('under_limit')
    values.append(str(round(project['credit'])))
    values.append(str(round(project['balance'])))
    values.append(str(round(project['used'])))
    values.append('"%s"'%','.join([m['username'] for m in project['members']]))
    
    values = ','.join(values)
    values.encode('utf8', 'ignore')
    print values

def print_projects(projects):
    for p in projects:
        values = []
        values.append(p['title'][:75])
        values.append(p['owner']['username'])
        values.append(p['name'])
        values.append(p['start_date'][:10])
        values.append(p['end_date'][:10])
        if p['over_limit']:
            values.append('over_limit')
        else:
            values.append('under_limit')
        values.append(str(round(p['credit'])))
        values.append(str(round(p['balance'])))
        values.append(str(round(p['used'])))
        values.append('"%s"'%','.join([m['username'] for m in p['members']]))
        
        values = ','.join(values)
        values.encode('utf8', 'ignore')
        print values

def print_projects_to_file(projects,output_filename):
    with open(output_filename,'w') as f:
        for p in projects:
            values = []
            values.append(p['title'][:75])
            values.append(p['owner']['username'])
            values.append(p['name'])
            values.append(p['start_date'][:10])
            values.append(p['end_date'][:10])
            if p['over_limit']:
                values.append('over_limit')
            else:
                values.append('under_limit')
            values.append(str(round(p['credit'])))
            values.append(str(round(p['balance'])))
            values.append(str(round(p['used'])))
            values.append('"%s"'%','.join([m['username'] for m in p['members']]))
            values.append('\n')

            values = ','.join(values)
            f.write(values.encode('utf8', 'ignore'))
        f.close()


if __name__ == '__main__': 
    parser = optparse.OptionParser(description='Export project data as CSV.')

    parser.add_option('-d','--datalevel',
        help="""Specify how much data is exported.                               
        Data Level 0 (default) - Show only active, under-limit projects                                                         
        Data Level 1 - Show overdrawn and long-expired projects.                                         
        Data Level 2 - Show all known projects.
        """,
        action='store', default='0', choices=['0','1','2'])

    parser.add_option('--projectname', help='Display data for a single project.')
    parser.add_option('--outputfile', help='Prints data to the specified file instead of to the terminal.')

    options, args = parser.parse_args()

    if (options.datalevel == '2') or options.projectname:
        request_url = REQUEST_URL%'all'
    else:
        request_url = REQUEST_URL%'ucb'
    try:
        data = urllib2.urlopen(request_url)
    except urllib2.HTTPError:
        print 'HTTP request failed:\nIs the server down, or overloaded?\n'
        sys.exit(1)
    projects = json.load(data)

    if options.projectname:
        exists = False
        for i in range(0,len(projects)):
            if projects[i]['name'] == options.projectname:
                print_single_project(projects[i])
                exists = True
        if not exists:
            print 'Project %s not found.'%options.projectname
        sys.exit(0)


    if options.datalevel == '0':
        curr_epoch = (
            datetime.datetime.now()-datetime.datetime(1970,1,1)
            ).total_seconds()
        one_month = datetime.timedelta(seconds=2678400).total_seconds()

        for i in range(0,len(projects)):
            try:
                pdate = datetime.datetime.strptime(
                    projects[i]['end_date'],
                    '%Y-%m-%dT%H:%M:%S.%fZ'
                    )
            except ValueError:
                pdate = datetime.datetime.strptime(
                    projects[i]['end_date'],
                    '%Y-%m-%dT%H:%M:%SZ'
                    )
            proj_epoch = (pdate-datetime.datetime(1970,1,1)
            ).total_seconds()

            if (curr_epoch-proj_epoch) > one_month:
                projects.pop(i)

        for i in range(0,len(projects)):
            try:
                if projects[i]['over_limit']:
                    projects.pop(i)
            except IndexError:
                break

    if not options.outputfile:
        print_projects(projects)
    else:
        print_projects_to_file(projects,options.outputfile)
