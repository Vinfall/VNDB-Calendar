#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Documentation
# VNDB API: https://api.vndb.org/kana#post-ulist

# One-liner
# get default/custom label id
# curl 'https://api.vndb.org/kana/ulist_labels?user=u1'
# get ulist
# curl https://api.vndb.org/kana/ulist --header 'Content-Type: application/json' --data $data | jq .

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timedelta

import dateparser
import requests
from ics import Calendar, Event

# import importlib
# Import functions from vndb_calendar
# vndb_module = importlib.import_module("vndb_calendar")

# Output files
_OUTPUT_FOLDER = "output/"
_CSV_FILE = "wishlist.txt"
_JSON_FILE = "wishlist.json"
_ICS_FILE = "wishlist.ics"

# Date format
# _SHIFT_TIME = "today"
_SHIFT_TIME = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")
# Mid year
_MID_YEAR = "-09-15"
_YEAR_ONLY_REGEX = "^(\\d{4})$"
_YYYYMM_ONLY_REGEX = "^(\\d{4}-\\d{2})$"

# Query parameters
FIELDS = "id, vn.title, vn.released"

default_filters = [
    "and",
    # wishlist is 5, custom label may have different id
    # private label requires authentication
    ["label", "=", 5],
    ["released", "!=", "TBA"],
]

default_data = {
    "user": "u2",
    "fields": FIELDS,
    "filters": default_filters,
    "sort": "released",
    "reverse": True,
    "results": 100,
    "page": 1,
}


# Arguments for easy customization
wishlist_parser = argparse.ArgumentParser()
# 2 is sufficient enough in most cases
wishlist_parser.add_argument(
    "-p",
    "--max-page",
    type=int,
    required=False,
    default=1,
    help="max pages of query results",
)
wishlist_parser.add_argument(
    "-u",
    "--user",
    type=str,
    required=True,
    default="u2",
    help="user id with 'u', e.g. 'u2'",
)
args = wishlist_parser.parse_args()


def get_page(max_page, data):
    api_url = "https://api.vndb.org/kana/ulist"
    headers = {"Content-Type": "application/json"}
    all_results = []

    # Parse parameters
    data["user"] = args.user

    for page in range(1, max_page + 1):
        data["page"] = page

        response = requests.post(
            api_url, data=json.dumps(data), headers=headers, timeout=15
        )

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
        # Build new json
        processed_result = {
            "id": result["id"],
            "released": result["vn"]["released"],
            "title": result["vn"]["title"],
        }
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
        # Do not save lengthy intro
        fields_to_save = ["id", "title", "released"]
        # Use semi-column seperator to avoid mismatches
        writer = csv.DictWriter(csv_file, fieldnames=fields_to_save, delimiter=";")

        writer.writeheader()
        for result in processed_results:
            # Compact fields
            selected_data = {field: result[field] for field in fields_to_save}
            writer.writerow(selected_data)

    return processed_results


# Function borrowed from SteamWishlistCalendar
# https://github.com/icue/SteamWishlistCalendar/blob/166cc44fec28b01771ac39def0a340940d2a5bf3/swc.py#L34-L52
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

    # Subtracte 1 day from the first day of the next next month, to get the last day of next month.
    return datetime(year, next_next_month, 1) - timedelta(days=1)


# Make calendar
def make_calendar(processed_results):
    cal = Calendar(creator="VNDBWishlistCalendar")
    now = datetime.now()
    event_dict = {}

    for result in processed_results:
        description_suffix = ""
        vnid = result["id"]
        vid = vnid[1:]
        title = result["title"]
        release_date = result["released"]
        url = "https:///vndb.org/" + vid

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
                # If the estimated release date has already passed,
                # pick the earliest upcoming last-of-a-month date
                release_date = last_day_of_next_month(release_date)
                # Only show estimation message in above cases
                description_suffix = f'\nEstimated on "{result["released"]}"'

        # Ensure release_date is a datetime object
        if isinstance(release_date, str):
            release_date = datetime.strptime(release_date, "%Y-%m-%d")

        description = url + description_suffix
        event = Event(
            uid=vid,
            summary=title,
            description=description,
            begin=release_date,
            last_modified=now,
            dtstamp=now,
            categories=["vn_wishlist"],
        )
        event.make_all_day()

        # Only append events if it's a different VN
        # Do NOT use release_date as a VN can have multiple releases on different dates
        key = (vid, title)
        if key not in event_dict:
            event_dict[key] = event
    for event in event_dict.values():
        cal.events.append(event)

    with open(_OUTPUT_FOLDER + _ICS_FILE, "w", encoding="utf-8") as f:
        f.write(cal.serialize())


os.makedirs(_OUTPUT_FOLDER, exist_ok=True)
j = get_page(args.max_page, default_data)
res = process_json(j)
make_calendar(res)
