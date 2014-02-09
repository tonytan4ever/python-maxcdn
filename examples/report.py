#!/usr/bin/env python
import pprint as pp
from os import environ as env
from maxcdn import MaxCDN

try:
    report = "/"+argv[1]
except:
    report = ""

if not "ALIAS" in env or not "KEY" in env or not "SECRET" in env:
    print(dedent("""\
        Usage: report.py [monthly|daily|hourly]

          Add credentials to your environment like so:

          $ export ALIAS=<alias>
          $ export KEY=<key>
          $ export SECRET=<secret>
        """))
    exit(1)


maxcdn = MaxCDN(env["ALIAS"], env["KEY"], env["SECRET"])

zones = maxcdn.get("/zones/pull.json")
for zone in zones["data"]["pullzones"]:
    print("Zone report for: %s (%s)" % (
        zone["name"], zone["url"]))

    # summary
    fetch = maxcdn.get("/reports/%s/stats.json%s" % (zone["id"], report))
    for key, val in fetch["data"]["summary"].iteritems():
        print(" - %s: %s" % (key, val))

    # popularfiles
    print(" ")
    print("Popular Files:")

    fetch = maxcdn.get("/reports/%s/popularfiles.json?page_size=10" % (zone["id"]))
    for file in fetch["data"]["popularfiles"]:
        print(" - url: " + file["uri"])
        print("   - hits: " + file["hit"])
        print("   - size: " + file["size"])

    print(" ")

