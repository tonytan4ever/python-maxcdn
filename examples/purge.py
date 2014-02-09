#!/usr/bin/env python
import pprint   as pp
from   os       import environ as env
from   sys      import exit, argv
from   textwrap import dedent
from   maxcdn   import MaxCDN

try:
    zoneid = argv[1]
except:
    zoneid = None

if not "ALIAS" in env or not "KEY" in env or not "SECRET" in env:
    print(dedent("""\
        Usage: purge.py zoneid

          Add credentials to your environment like so:

          $ export ALIAS=<alias>
          $ export KEY=<key>
          $ export SECRET=<secret>
        """))
    exit(1)

maxcdn = MaxCDN(env["ALIAS"], env["KEY"], env["SECRET"])

if zoneid is None:
    zones = maxcdn.get("/zones/pull.json")
    for zone in zones["data"]["pullzones"]:
        print("Purging zone: %s (%s)" % (
            zone["name"], zone["id"]))

        pp.pprint(maxcdn.purge(zone["id"]))
else:
    print("Purging zone: %s" % (zoneid))
    res = maxcdn.purge(zoneid)
    try:
        if res["code"] == 200:
            print("SUCCESS!")
        else:
            print("Failed with code: " + res["code"])
            exit(res["code"])
    except KeyError:
        print("Something went terribly wrong!")
        pp.pprint(res)
        exit(1)

