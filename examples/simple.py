#!/usr/bin/env python
import pprint as pp
from os       import environ as env
from maxcdn   import MaxCDN
from textwrap import dedent

if not "ALIAS" in env or not "KEY" in env or not "SECRET" in env:
    print(dedent("""\
        Usage: simple.py

          Add credentials to your environment like so:

          $ export ALIAS=<alias>
          $ export KEY=<key>
          $ export SECRET=<secret>
    """))
    exit(1)

maxcdn = MaxCDN(env["ALIAS"], env["KEY"], env["SECRET"])

print("GET '/account.json'")
pp.pprint(maxcdn.get("/account.json"))

print("GET '/account.json/address'")
pp.pprint(maxcdn.get("/account.json/address"))

print("GET '/reports/stats.json/hourly'")
pp.pprint(maxcdn.get("/reports/stats.json/hourly"))

