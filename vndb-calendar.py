#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation
# VNDB API: https://api.vndb.org/kana#post-release
# ICS: https://icspy.readthedocs.io/en/stable/api.html#event
# Dateparser: https://dateparser.readthedocs.io/en/latest/#incomplete-dates

import os
import sys
import dateparser
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
    "();",
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

# TODO: Alternatively, use compact filter to get rid of all weirdness
# Side effect: no time shift
# filters = "0672171_4YsVe132gja2wzh_dHans-2wzh_dHant-N48721gwcomplete-N480281UJ81Xkx"

"""
# TODO: Remove BLG
# Side effect: VNs with no tag would be filtered out as well
(
    [
        "vn",
        "!=",
        [
            "any",
            ["tag", "=", "g542"],
            ["tag", "=", "g2002"],
            # This would filter out girl x girl romance as well, find a better way
            ["tag", "=", ["g134", 2, 1.4]],
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
    # Not sure why /vn does not work well with "released" filter so use /release instead
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

    # Save results to JSON file
    with open(
        f"{_OUTPUT_FOLDER + _JSON_FILE}",
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(processed_results, file, ensure_ascii=False, indent=2)

    # Save results to CSV file
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


# Function borrowed from SteamWishlistCalendar
# https://github.com/icue/SteamWishlistCalendar/blob/b5995dd44e8a0e682e80962277bc905eed744768/swc.py#L33-L51
def last_day_of_next_month(dt):
    """
    Returns the datetime of the last day of the next month.

    Args:
    dt: A datetime.datetime object.

    Returns:
    A datetime.datetime object.
    """

    year = dt.year
    next_next_month = dt.month + 2
    if next_next_month > 12:
        next_next_month -= 12
        year = dt.year + 1

    # Subtracting 1 day from the first day of the next next month, to get the last day of next month.
    return datetime(year, next_next_month, 1) - timedelta(days=1)


# Make calendar
def make_calendar(processed_results):
    cal = Calendar(creator="VNDBRelCalendar")
    now = datetime.now()
    event_dict = {}

    for result in processed_results:
        description_suffix = ""
        vid = result["vid"]

        # Parse date to better fit into reality
        release_date = dateparser.parse(
            result["released"],
            settings={
                "PREFER_DAY_OF_MONTH": "last",
                "PREFER_DATES_FROM": "future",
                "PREFER_MONTH_OF_YEAR": "last",
            },
        )
        while release_date.date() < now.date():
            # If the estimated release date has already passed, pick the earliest upcoming last-of-a-month date
            release_date = last_day_of_next_month(release_date)
            # Only show estimation message in above cases
            description_suffix = f'\nEstimated on "{release_date}"'

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
