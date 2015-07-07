#!/bin/env python

import sys
import urllib
import argparse
import xml.etree.ElementTree as ET

def check_pool(server,pool):
    url='http://%s:2288/webadmin/info?statepath=pools/%s'%(server,pool)

    f = urllib.urlopen(url)
    myfile = f.read()
    #print myfile
    root=ET.fromstring(myfile)

    enabled=bool(root[0][0][0].text)

    total=int(root[0][0][3][1][0].text)
    queued=int(root[0][0][3][1][1].text)
    active=int(root[0][0][3][1][2].text)
    return (enabled,total,queued,active)

OK_EXIT_CODE=0
WARN_EXIT_CODE=1
CRIT_EXIT_CODE=2

parser = argparse.ArgumentParser(description='Check running/queued movers for pools.')
parser.add_argument('-s', '--server', metavar='SERVER', type=str, required = True,
                   help='dCache server to contact')
parser.add_argument('-p', '--pools', metavar='POOLS', type=str, required = True,
                   help='list of pools to check. comma (and no space) separated. eg. pool1_1,pool1_2,pool1_3')
parser.add_argument('-w', '--warning', metavar='WARNING', type=int, required = True,
                   help='=threshold for warning of the queued movers')
parser.add_argument('-c', '--critical', metavar='CRITICAL', type=int, required = True,
                   help='=threshold for critical of the queued movers')
parser.add_argument('-v', '--verbose', action='store_true', default = False,
                   help='dCache server to contact')

args = parser.parse_args()
server=args.server
pools=args.pools.split(',')
warning_threshold=args.warning
critical_threshold=args.critical
verbose=args.verbose

res={}
for p in pools:
    res[p]=(check_pool(server,p))
if verbose:
    print 'POOL NAME\tENABLED\tTOTAL\tQUEUED\tACTIVE'

crit=[]
warn=[]
disabled=[]
for p in res.keys():
    vals=res[p]
    if verbose:
        print '%s\t%s\t%s\t%s\t%s'%(p,vals[0],vals[1],vals[2],vals[3])
    if vals[0]==False:
        disabled.append(p)
    if vals[2]>critical_threshold:
        crit.append(p)
    elif vals[2]>warning_threshold:
        warn.append(p)

if len(disabled)>0:
    print 'CRITICAL: The following pools are disabled:'
    for p in disabled:
        print p

if len(warn)>0:
    print 'WARNING: The following pools have more than %s queued movers:'%warning_threshold
    for p in warn:
        print p

if len(crit)>0:
    print 'CRITICAL: The following pools have more than %s queued movers:'%critical_threshold
    for p in crit:
        print p

if len(disabled)>0 or len(crit)>0:
    sys.exit(CRIT_EXIT_CODE)

if len(warn)>0:
    sys.exit(WARN_EXIT_CODE)

print "All pools are OK"
sys.exit(OK_EXIT_CODE)
