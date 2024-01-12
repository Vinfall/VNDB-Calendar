#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation
# VNDB API: https://api.vndb.org/kana#post-release
# ICS: https://icspy.readthedocs.io/en/stable/api.html#event
# Dateparser: https://dateparser.readthedocs.io/en/latest/settings.html#handling-incomplete-dates

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

# Date format
# _SHIFT_TIME = "today"
_SHIFT_TIME = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
# Mid year
_MID_YEAR = "-09-15"
_YEAR_ONLY_REGEX = "^(\\d{4})$"
_YYYYMM_ONLY_REGEX = "^(\\d{4}-\\d{2})$"

# Block word list full of hacky regex
_TO_REPLACE = [
    "\\(\\);",  # A special case for v33120
    "(Windows)? パッケージ(特装)?(初回)?版",
    " ダウンロード(通常)?(豪華)?版",
    " オナホール同梱版",
    " ダブルパック",
    " (通常)?DL(通常)?(カード)?版",
    " (通常)?PK版",
    # " 通常DL版",
    " デラックス(DL)?(PK)?版",
    " PK版 デラックス版",
    " - .*? Version$",
    # " - .*? Patch$",
    "Normal Edition",
    " 単体版",
    " 通常版",
    " 特典版",
    " (完全生産)?限定版",
    " 豪華(限定)?(特装)?版",
    " 初回(限定)?(特典)?版",
]

# Query parameters
# fields = "id,title,alttitle,languages.mtl,platforms,media,vns.rtype,producers,released,minage,patch,uncensored,official,extlinks"
fields = "id, title, alttitle, released, vns.id"
# This is sufficient enough in most cases
max_page = 2

# To get normalized filters from compact one:
# curl https://api.vndb.org/kana/release --json '{"filters":my_filters,"normalized_filters":true,"results":0}'


filters = [
    "and",
    # Comment the line below to show all language releases
    ["or", ["lang", "=", "ja"], ["lang", "=", "zh-Hans"], ["lang", "=", "zh-Hant"]],
    # ["olang", "=", "ja"],
    ["released", "!=", "TBA"],
    ["released", ">=", _SHIFT_TIME],
    ["vn", "=", ["and", ["released", ">=", _SHIFT_TIME]]],
    ["rtype", "=", "complete"],
    # Comment filters below to unhide BLG/Otome games
    [
        "vn",
        "=",
        [
            "and",
            ["tag", "!=", "g542"],
            ["tag", "!=", "g2002"],
            # This would filter out girl x girl romance as well, find a better way
            # ["tag", "!=", ["g134", 2, 1.4]],
        ],
    ],
    # More unintended tags
    [
        "vn",
        "=",
        [
            "and",
            ["tag", "!=", "g83"],
            ["tag", "!=", "g117"],
            ["tag", "!=", "g161"],
            ["tag", "!=", "g897"],
            ["tag", "!=", "g1300"],
            ["tag", "!=", "g3084"],
        ],
    ],
]

# Alternatively, use compact filter to get rid of all weirdness
# Side effect: no time shift
# filters = "0672171_4YsVe132gja2wzh_dHans-2wzh_dHant-N48721gwcomplete-N480281UJ81Xkx"


data = {
    "filters": filters,
    "fields": fields,
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
    # Reasons not using /vn
    # 1. not working well with "released" filter
    # 2. too many alttitles, or no alttitle at all
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
        # Replace trailing release variations like `ダウンロード版` and `DLカード版`
        for keyword in _TO_REPLACE:
            processed_result["title"] = re.sub(keyword, "", processed_result["title"])

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
        title = result["title"]
        release_date = result["released"]

        # Parse date to better fit into reality
        # Match release date like `2026`
        year_only_match = re.match(_YEAR_ONLY_REGEX, release_date)
        if year_only_match:
            year = year_only_match.group(1)
            # If Sep 15 of this year passed, use the end of year
            mid_release_date = datetime.strptime(year + _MID_YEAR, "%Y-%m-%d").date()
            release_date = year + (
                _MID_YEAR if mid_release_date > now.date() else "-12-31"
            )
            description_suffix = f'\nEstimated on "{result["released"]}"'
        # Complete remaining release date like `2024-03`
        yyyymm_only_match = re.match(_YYYYMM_ONLY_REGEX, release_date)
        if yyyymm_only_match:
            release_date = dateparser.parse(
                release_date,
                settings={
                    "PREFER_DAY_OF_MONTH": "last",
                    "PREFER_DATES_FROM": "future",
                },
            )
            while release_date.date() < now.date():
                # If the estimated release date has already passed, pick the earliest upcoming last-of-a-month date
                release_date = last_day_of_next_month(release_date)
                # Only show estimation message in above cases
                description_suffix = f'\nEstimated on "{result["released"]}"'

        # TODO: include more info
        event = Event(
            uid=vid,
            name=title,
            description="https://vndb.org/" + vid + description_suffix,
            begin=release_date,
            last_modified=now,
            categories=["vn_release"],
        )
        event.make_all_day()

        # Only add events if it's a different VN
        # Do NOT use release_date as a VN can have multiple releases on different dates
        key = (vid, title)
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
