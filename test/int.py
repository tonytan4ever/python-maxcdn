#!/usr/bin/env python
import unittest
import re
import time
import os

from maxcdn import MaxCDN

class MaxCDNIntegration(unittest.TestCase):

    def setUp(self):
        self.alias   = os.environ["ALIAS"]
        self.key     = os.environ["KEY"]
        self.secret  = os.environ["SECRET"]
        self.time    = str(int(time.mktime(time.gmtime())))

        self.max     = MaxCDN(self.alias, self.key, self.secret)

    def test_get(self):
        for end_point in [ "account.json", "account.json/address", "users.json", "zones.json" ]:
            if "/" in end_point:
                key = end_point.split("/")[1]
            else:
                key = end_point.replace(".json", "")

            res = self.max.get(end_point)
            self.assertTrue(res["data"][key], "get "+key+" with data")

    def test_post_and_delete(self):
        data = { "name": self.time, "url": "http://www.example.com/" }
        res  = self.max.post("/zones/pull.json", data=data)
        zid  = str(res["data"]["pullzone"]["id"])

        self.assertTrue(zid, "post")
        self.assertEqual(200, self.max.delete("/zones/pull.json/"+zid)["code"], "delete")

    def test_put(self):
        street = self.time + "_put"
        self.assertEqual(street, str(self.max.put("/account.json/address", { "street1": street })["data"]["address"]["street1"]))

    def test_purge(self):
        zone = self.max.get("zones/pull.json")["data"]["pullzones"][0]["id"]
        self.assertEqual(200, self.max.purge(zone)["code"])

        popularfiles = self.max.get("reports/popularfiles.json")["data"]["popularfiles"]

        self.assertEqual(200, self.max.purge(zone, popularfiles[0]["uri"])["code"])
        self.assertEqual(200, self.max.purge(zone, [ popularfiles[0]["uri"], popularfiles[1]["uri"]])["code"])

if __name__ == '__main__':
        unittest.main()
