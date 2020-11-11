#! /usr/bin/python3

import os, sys

sys.path.append(os.path.join(os.environ['alfred_preferences'], 'workflows'))

import json
import urllib.parse

import alfred
import iso8601

from datetime import timedelta, datetime
from babel.dates import format_timedelta

class Device(dict):
    def __init__(self, device):
        dict.__init__(self)

        self["title"] = device["name"]

        recentAccessDate = device["recentAccessDate"]

        if recentAccessDate is not None:
            recentAccessDate = iso8601.parse_date(recentAccessDate)
            recentAccessDate = format_timedelta(
                    datetime.now() - recentAccessDate.replace(tzinfo=None),
                    locale='en_US'
                    )
            self["subtitle"] = recentAccessDate + " ago"

        self["uid"] = "bt-device." + device["address"]
        self["arg"] = device["address"]


option = sys.argv[1]

device_json = alfred.pipeline(
        [
            "blueutil",
            f"--{option}",
            "--format=json",
            ]
        )

raw_devices = json.loads(device_json)

item_outputter = alfred.ItemOutputter(raw_devices, Device)
item_outputter.process()
