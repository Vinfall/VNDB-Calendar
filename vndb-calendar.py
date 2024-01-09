#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation: https://api.vndb.org/kana#post-release

import os
import sys
from datetime import datetime
from datetime import timedelta
import requests
import json
import csv
from ics import Calendar, Event

# Output files
_OUTPUT_FOLDER = "output/"
_CSV_FILE = "vndb-release.txt"
_JSON_FILE = "vndb-release.json"
_ICS_FILE = "vndb-rel-calendar.ics"
# _SHIFT_TIME = "today"
_SHIFT_TIME = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# Query parameters
api_url = "https://api.vndb.org/kana/release"
# fields = "id,title,alttitle,languages.mtl,platforms,media,vns.rtype,producers,released,minage,patch,uncensored,official,extlinks"

filters = [
    "and",
    # Comment the line below to show all language releases
    ["or", ["lang", "=", "ja"], ["lang", "=", "zh-Hans"], ["lang", "=", "zh-Hant"]],
    # ["olang", "=", "ja"],
    ["released", "!=", "TBA"],
    ["released", ">=", _SHIFT_TIME],
    ["vn", "=", ["and", ["released", ">=", _SHIFT_TIME]]],
    ["rtype", "=", "complete"],
]

"""
# TODO: Remove BLG
(
    [
        "vn",
        "!=",
        [
            "any",
            ["tag", "=", ["g134", 2, 1.4]],
            ["tag", "=", ["g542"]],
            ["tag", "=", ["g2002"]],
        ],
    ],
)
"""


data = {
    "filters": filters,
    "fields": "id, title, alttitle, released",
    "sort": "released",
    "reverse": False,
    "results": 100,
    "page": 1,
    # "user": "null",
    # "count": False,
    "compact_filters": False,
    "normalized_filters": True,
}


def get_page(url, data):
    headers = {"Content-Type": "application/json"}
    response = requests.post(url, data=json.dumps(data), headers=headers)
    if response.status_code == 200:
        print("Post request successful")
        return response.json()
    else:
        print("Post request failed")
        print(response)
        sys.exit()


# Process & Write results to JSON & CSV
def process_json(json_data):
    results = json_data["results"]

    processed_results = []
    for result in results:
        processed_result = {
            "id": result["id"],
            "released": result["released"],
        }
        if result["alttitle"] is not None:
            processed_result["title"] = result["alttitle"]
        else:
            processed_result["title"] = result["title"]
        processed_results.append(processed_result)

    with open(
        f"{_OUTPUT_FOLDER + _JSON_FILE}",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(processed_results, file, ensure_ascii=False, indent=2)

    with open(
        _OUTPUT_FOLDER + _CSV_FILE, mode="w", newline="", encoding="utf-8"
    ) as csv_file:
        fieldnames = ["id", "title", "released"]
        # Use semi-column seperator to avoid mismatches
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=";")

        writer.writeheader()
        for result in processed_results:
            writer.writerow(result)

    return processed_results


# Make calendar
def make_calendar(processed_results):
    cal = Calendar(creator="VNDB-RelCalendar")
    now = datetime.now()
    event_dict = {}

    for result in processed_results:
        vn_name = result["title"]
        description_suffix = ""
        release_date = result["released"]

        # TODO: include more info
        event = Event(
            uid=result["id"],
            name=vn_name,
            description="https://vndb.org/" + result["id"] + description_suffix,
            begin=release_date,
            last_modified=now,
            categories=["vn_release"],
        )
        event.make_all_day()

        # Only add events if we don't have any
        key = (vn_name, release_date)
        if key not in event_dict:
            event_dict[key] = event
    for event in event_dict.values():
        cal.events.add(event)

    with open(_OUTPUT_FOLDER + _ICS_FILE, "w", encoding="utf-8") as f:
        f.write(cal.serialize())


os.makedirs(_OUTPUT_FOLDER, exist_ok=True)
j = get_page(api_url, data)
results = process_json(j)
make_calendar(results)
