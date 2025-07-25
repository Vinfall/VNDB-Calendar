#!/usr/bin/env python3

# Documentation
# VNDB API: https://api.vndb.org/kana#post-release
# VNDB Formatting Codes: https://vndb.org/d9#4
# ICS: https://icspy.readthedocs.io/en/stable/api.html#event
# Argparse: https://docs.python.org/3/library/argparse.html
# Dateparser: https://dateparser.readthedocs.io/en/latest/settings.html#handling-incomplete-dates

import argparse
import csv
import json
import os
import re
import sys
from datetime import datetime, timedelta
from typing import Any

import dateparser
import requests
from ics import Calendar, Event

# Output files
_OUTPUT_FOLDER = "output/"
_CSV_FILE = "vndb-release.txt"
_JSON_FILE = "vndb-release.json"
_ICS_FILE = "vndb-calendar.ics"

# Date format
# _SHIFT_TIME = "today"
_SHIFT_TIME = (datetime.now() - timedelta(days=14)).strftime("%Y-%m-%d")  # noqa: DTZ005
# Mid year
_MID_YEAR = "-09-15"
_YEAR_ONLY_REGEX = "^(\\d{4})$"
_YYYYMM_ONLY_REGEX = "^(\\d{4}-\\d{2})$"

# Block word list full of hacky regex
_TO_REPLACE = [
    "(Windows)?( )?パッケージ(特装)?(初回)?版",
    "( )?ダウンロード(通常)?(特装)?(豪華)?(カード)?版",
    " オナホール同梱版",
    " ダブルパック",
    " (超)?スタァライト(EDITION)?(版)?",
    " (豪華)?(通常)?(DL|ＤＬ|パッケージ)(通常)?(カード)?版",
    " (豪華)?(通常)?PK版",
    "パッケージ",
    # " 通常DL版",
    " プレミアム版",
    " デラックス(DL)?(PK)?版",
    " PK版 デラックス版",
    " デジタルデラックスエディション",
    "( )?- .*? Version$",
    "( )?- .*? Edition$",
    " (Download|Standard|Package) Edition",
    # "( )?- .*? Patch$",
    # " ~ 追加エピソード",
    "Normal Edition",
    " 単体版",
    " 通常版",
    " 特[典|装]版",
    " (超)?(特別)?(完全生産)?限定版",
    " 抱き枕カバー(付き)?(.*)?",
    "( )?豪華(限定)?(特装)?版",
    "( )?初回(限定)?(特典)?(特装)?版",
    " 数量限定(.*)?版",
    # Special cases
    # " Episode:[0-9].*?$",  # VenusBlood series
    " ボイスドラマ付き限定版",  # v51288
    " のぞみ初恋BOX",  # v55885
    " タペストリー付属版",  # v51309
    " スペシャルボックス",  # v50614
    " DLsite限定版",  # v53297
    " 特典付き限定版",  # v54776
    " 特典付限定版",  # v55358
]
# Normalize character (full -> half width)
_TO_REPLACE_WIDTH = (
    ("　", " "),
    ("～", "~"),
    ("！", "!"),
    ("？", "?"),
    # ("×", " x "),
)

# Query parameters
# FIELDS = "id,title,alttitle,languages.mtl,platforms,media,
#           vns.rtype,producers,released,minage,patch,uncensored,official,extlinks"
FIELDS = "id, title, alttitle, released, vns.id"

# To get normalized filters from compact one:
# curl https://api.vndb.org/kana/release --json '{"filters":my_filters,"normalized_filters":true,"results":0}'

# Alternatively, use compact filter to get rid of all weirdness
# Side effect: no time shift
# filters = "0672171_4YsVe132gja2wzh_dHans-2wzh_dHant-N48721gwcomplete-N480281UJ81Xkx"

_RTYPE_COMPLETE_FILTER = ["rtype", "=", "complete"]
_RTYPE_PARTIAL_FILTER = ["or", ["rtype", "=", "partial"], ["rtype", "=", "complete"]]

# fmt: off
_TAG_ID_FILTER = [
    7, 83, 117, 153, 161, 358, 897, 937, 988,
    1300, 1462, 2051, 2548, 3084, 3105, 3391, 3684
]
_PROD_ID_FILTER = [
    # Bad scenario / nukige
    215, 918, 1873, 1976, 2107, 2320, 2667, 3337, 4019, 4488, 5321, 5402, 7234,
    11502, 11860, 12518, 13110, 13155,
    # Personal preferences
    65, 200, 226, 507, 1463, 1741, 3489, 4680, 5008, 7573, 7812,
    10984, 11642, 11959, 13454, 13679, 18430, 20086, 20682,
    # AIGC / photographic
    20359, 20456, 20544, 20602, 22932,
    # Otome game
    567, 15102
]
# fmt: on


default_filters = [
    "and",
    # Comment the line below to show all language releases
    ["or", ["lang", "=", "ja"], ["lang", "=", "zh-Hans"], ["lang", "=", "zh-Hant"]],
    # ["olang", "=", "ja"],
    ["released", "!=", "TBA"],
    ["released", ">=", _SHIFT_TIME],
    ["vn", "=", ["and", ["released", ">=", _SHIFT_TIME]]],
    _RTYPE_COMPLETE_FILTER,  # 分割商法
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
            # Loop through all tag ids in the list
            *[["tag", "!=", f"g{i}"] for i in _TAG_ID_FILTER],
        ],
    ],
    # No Da Capo/NEKOPARA/Sakura series, and much more
    [
        "producer",
        "=",
        [
            "and",
            # Loop through all producer ids in the list
            *[["id", "!=", f"p{i}"] for i in _PROD_ID_FILTER],
        ],
    ],
]

default_data = {
    "filters": default_filters,
    "fields": FIELDS,
    "sort": "released",
    "reverse": False,
    "results": 100,
    "page": 1,
    # "user": "null",
    # "count": False,
    "compact_filters": False,
    "normalized_filters": True,
}


# Arguments for easy customization
parser = argparse.ArgumentParser()
parser.add_argument(
    "-f",
    "--filter",
    required=False,
    default=default_filters,
    help="custom compact filter, see https://api.vndb.org/kana#filters",
)
# 2 is sufficient enough in most cases
parser.add_argument(
    "-p",
    "--max-page",
    type=int,
    required=False,
    default=2,
    help="max pages of query results",
)
parser.add_argument(
    "-t",
    "--shift-time",
    type=int,
    required=False,
    default=None,
    help='show "new" releases X days ago, it\'s really upcoming release if set to 0',
)
parser.add_argument(
    "-d",
    "--description",
    "--intro",
    type=bool,
    required=False,
    default=False,
    help="add VN description to calendar event",
)
parser.add_argument(
    "-b",
    "--partial",
    "--beta",
    type=bool,
    required=False,
    default=False,
    help="show partial releases in query results",
)
args = parser.parse_args()


def get_page(max_page: int, data: dict[str, Any]) -> list[dict[str, Any]]:
    # Reasons not using /vn
    # 1. not working well with "released" filter
    # 2. too many alttitles, or no alttitle at all
    api_url = "https://api.vndb.org/kana/release"
    headers = {"Content-Type": "application/json"}
    all_results = []

    # Parse parameters
    # Use custom time shift, if any
    if args.shift_time:
        shift_time_new = (
            datetime.now() - timedelta(days=args.shift_time)  # noqa: DTZ005
        ).strftime("%Y-%m-%d")
        data["filters"] = args.filter.replace(_SHIFT_TIME, shift_time_new)
    # Add partial release on demand
    elif args.partial:
        data["filters"] = [
            _RTYPE_PARTIAL_FILTER if item == _RTYPE_COMPLETE_FILTER else item
            for item in args.filter
        ]
    # Or use the default value
    else:
        data["filters"] = args.filter
    # Add intro if related parameter is set
    if args.description:
        data["fields"] = "id, title, alttitle, released, vns.id, vns.description"

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
def process_json(results: list[dict[str, Any]]) -> list[dict[str, Any]]:
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
        if args.description:
            first_vns_intro = vns_ids[0]["description"] if vns_ids else ""
            processed_result["intro"] = first_vns_intro
        # Prefer alternative title, if available
        if result["alttitle"] is not None:
            processed_result["title"] = result["alttitle"]
        else:
            processed_result["title"] = result["title"]
        # Replace trailing release variations like `ダウンロード版` and `DLカード版`
        for keyword in _TO_REPLACE:
            processed_result["title"] = re.sub(keyword, "", processed_result["title"])
        # Replace full width characters with normal ones
        for pair in _TO_REPLACE_WIDTH:
            processed_result["title"] = re.sub(
                pair[0], pair[1], processed_result["title"]
            )
            if args.description and processed_result["intro"]:
                processed_result["intro"] = re.sub(
                    pair[0], pair[1], processed_result["intro"]
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
        # Do not save lengthy intro
        fields_to_save = ["vid", "id", "title", "released"]
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
def last_day_of_next_month(dt: datetime) -> datetime:
    """
    Return the datetime of the last day of the next month.

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
    return datetime(year, next_next_month, 1) - timedelta(days=1)  # noqa: DTZ001


# Make calendar
def make_calendar(processed_results: list[dict[str, Any]]) -> None:
    cal = Calendar(creator="VNDBCalendar")
    now = datetime.now()  # noqa: DTZ005
    event_dict = {}

    for result in processed_results:
        description_suffix = ""
        vid, rid, title, release_date = (
            result["vid"],
            result["id"][1:],  # TODO: err in game bundle (is a fix even possible?)
            result["title"],
            result["released"],
        )
        url = "https:///vndb.org/" + vid

        # Parse date to better fit into reality
        # Match release date like `2026`
        year_only_match = re.match(_YEAR_ONLY_REGEX, release_date)
        if year_only_match:
            year = year_only_match.group(1)
            # If Sep 15 of this year passed, use the end of year
            mid_release_date = datetime.strptime(  # noqa: DTZ007
                year + _MID_YEAR, "%Y-%m-%d"
            ).date()
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
            release_date = datetime.strptime(release_date, "%Y-%m-%d")  # noqa: DTZ007

        if args.description and result["intro"]:
            description = url + "\n" + result["intro"] + description_suffix
        else:
            description = url + description_suffix
        # TODO: include more info
        event = Event(
            uid=rid,  # release identifier is more unique, but would conflict with event_dict below
            summary=title,
            description=description,
            begin=release_date,
            last_modified=now,
            dtstamp=now,
            categories=["vn_release"],
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
