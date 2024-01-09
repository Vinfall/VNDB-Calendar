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
import re
from ics import Calendar, Event

# Output files
_OUTPUT_FOLDER = "output/"
_CSV_FILE = "vndb-release.txt"
_JSON_FILE = "vndb-release.json"
_ICS_FILE = "vndb-rel-calendar.ics"
# _SHIFT_TIME = "today"
_SHIFT_TIME = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
# Block word list, not sure why regex not working
_TO_REPLACE = [
    " パッケージ版",
    " パッケージ特装版",
    " パッケージ初回版",
    " ダウンロード版",
    " ダウンロード通常版",
    " ダウンロード豪華版",
    " オナホール同梱版",
    " DL版",
    " DL通常版",
    " DLカード版",
    " 通常DL版",
    " 通常PK版",
    " デラックスDL版",
    " デラックスPK版",
    " - Adult Version",
    " - Censored Version",
    " - Download Edition",
    " - Package Edition",
    " - Physical Edition",
    " 単体版",
    " 通常版",
    " 特典版",
    " 限定版",
    " 豪華版",
    " 初回版",
    " 豪華限定版",
    " 初回限定版",
    " 初回特典版",
    " 豪華特装版",
    " 完全生産限定版",
]

# Query parameters
# fields = "id,title,alttitle,languages.mtl,platforms,media,vns.rtype,producers,released,minage,patch,uncensored,official,extlinks"
# This is sufficient enough in most cases
max_page = 2

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
    "fields": "id, title, alttitle, released, vns.id",
    "sort": "released",
    "reverse": False,
    "results": 100,
    "page": 1,
    # "user": "null",
    # "count": False,
    "compact_filters": False,
    "normalized_filters": True,
}


def get_page(max_page, data):
    api_url = "https://api.vndb.org/kana/release"
    headers = {"Content-Type": "application/json"}
    all_results = []

    for page in range(1, max_page + 1):
        data["page"] = page
        response = requests.post(api_url, data=json.dumps(data), headers=headers)

        if response.status_code == 200:
            json_data = response.json()
            # Combine response
            if "results" in json_data:
                all_results.extend(json_data["results"])
            else:
                print("No results found for page ", page)
                print(response)
                break
        else:
            print("Post request failed")
            print(response)
            sys.exit()
    print("Post request successful")
    return all_results


# Process & Write results to JSON & CSV
def process_json(results):
    processed_results = []
    for result in results:
        # Convert list to single string in case release contains multiple VNs
        vns_ids = result.get("vns", [])
        first_vns_id = vns_ids[0]["id"] if vns_ids else None
        # Build new json
        processed_result = {
            "vid": first_vns_id,
            "id": result["id"],
            "released": result["released"],
        }
        # Prefer alternative title, if available
        if result["alttitle"] is not None:
            processed_result["title"] = result["alttitle"]
        else:
            processed_result["title"] = result["title"]
        # Replace release variated titles like `ダウンロード版` and `DLカード版`
        for keyword in _TO_REPLACE:
            processed_result["title"] = re.sub(
                re.escape(keyword), "", processed_result["title"]
            )

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
        fieldnames = ["vid", "id", "title", "released"]
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
        description_suffix = ""
        release_date = result["released"]
        vid = result["vid"]

        # TODO: include more info
        event = Event(
            uid=vid,
            name=result["title"],
            description="https://vndb.org/" + vid + description_suffix,
            begin=release_date,
            last_modified=now,
            categories=["vn_release"],
        )
        event.make_all_day()

        # Only add events if it's a different VN
        key = (vid, release_date)
        if key not in event_dict:
            event_dict[key] = event
    for event in event_dict.values():
        cal.events.add(event)

    with open(_OUTPUT_FOLDER + _ICS_FILE, "w", encoding="utf-8") as f:
        f.write(cal.serialize())


os.makedirs(_OUTPUT_FOLDER, exist_ok=True)
j = get_page(max_page, data)
results = process_json(j)
make_calendar(results)
