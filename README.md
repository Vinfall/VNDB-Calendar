# VNDB Calendar

[![Build](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/custom.yml/badge.svg)](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/custom.yml) [![Release](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/release.yml/badge.svg)](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/release.yml) [![Test](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/test.yml/badge.svg)](https://github.com/Vinfall/VNDB-Calendar/actions/workflows/test.yml)

中文介绍请看 [README_zh-Hans](README_zh-Hans.md)

## Intro

This tiny tool allows you to create a calendar of [VNDB](https://vndb.org) [upcoming releases](https://vndb.org/r?f=01731;o=a;s=released). Everything is supposed to be automated via GitHub Actions after initial setup. If you choose to publish the `ICS` file, you can just subscribe it in any calendar app that supports iCalendar.

[en](https://github.com/Vinfall/VNDB-Calendar/releases/download/en/vndb-calendar.ics) contains recent en & ja releases.
Similarly, [enpatch](https://github.com/Vinfall/VNDB-Calendar/releases/download/enpatch/vndb-calendar.ics) for unofficial en localization/content restoration patches.

## Why

For now VNDB only offers RSS for *Recent Changes*, but not *Upcoming Releases* or *Just Released*. There are multiple previous discussions about that but I don't think Yorhel is going to do that any time soon.

This is created as a workaround for personal use and serves as an extension of my blog post [iCalendar (ICS) 的养成方式](https://blog.vinfall.com/posts/2023/12/ics/) (written in Chinese).

## Usage

### Release Calendar

To customize the query, run [`vndb_calendar.py`](vndb_calendar.py) with optional parameters:
- `python vndb_calendar.py -f {customized_compact_filter} -p {max_page} -t {shift_time} -d {1 or 0} -b {0 or 1}`
- Example of generic filters for en & ja upcoming releases with description: `python vndb-calendar.py -f "0572171_4YsVe122gen2gjaN48721gwcomplete-" -t 0 -d 1 -b 0`
- `-f` or `--filter`: your custom [compact filters](https://api.vndb.org/kana#filters), by default it would use my personalized one
- `-p` or `--max-page`: maximum pages of query results, by default it will be `2`
- `-t` or `--shift-time`: show *new* releases X days ago, it's really upcoming release if set to `0`, by default it will be `14`
- `-d`, `--description` or `--intro`: add VN description to calendar event, bool type (only `0`/`1` is supported), by default `0`/`False`
- `-b`, `--beta` or `--partial`: show partial releases in query results, e.g. multiple chapters

### Wishlist Calendar

This is basically an inferior version of release calendar, focused on a user's wishlist.

Nothing to customize actually, simply run [`wishlist.py`](wishlist.py):
- `python wishlist.py -u "{uid}" -p {max_page}`
- Example of Yorhel's wishlist: `python wishlist.py -u "u2"`
- `-u` or `--user`: user id **with** 'u', e.g. `u2`
- `-p` or `--max-page`: maximum pages of query results, by default it will be `1`. As wishlist is fetched reversely, newest items come first. Each page has 100 items, so 1 page is usually suffecient if you use calendar only for upcoming releases.

> [!NOTE]
> `wishlist.py` assumes you use the default `wishlist` label and have not set it as private.
> If you prefer to use another default label or your custom labels to generate calendar,
> use attached one-liner to determine the label id and change `default_filters` in the script.

## TODO

- [x] Remove redundant releases of the same VN
- [x] Declutter common release variate titles like `ダウンロード版` and `DLカード版`
- [x] Better handling of incomplete date like `2026` and `2024-02`
- [x] Find out why many filters would make responses 400 (misplaced filter params)
- [x] Filter out BLG/Otome game & other tags I wish to avoid
- [x] Add filters arguments (you can use [compact filters](https://api.vndb.org/kana#filters) to quickly customize the results)
- [x] Make calendar with generic en & ja releases (in a tagged automated release)
- [x] Add VN description in calendar events and make it a parameter
- [x] Add user wishlist, just like SteamWishlistCalendar
- [x] Support partial releases
- [ ] Fix event parsing bug caused by `rid` & `event_dict`
- [ ] Do not use alternative title in en tagged release (low priority, I assume people would prefer literal title instead of confusing Romaji)
- [ ] Add external links (Getchu/DMM/DLsite/Steam/Official website etc.) to event description (low priority, quite long already with VN description)

## Contribution

If you happen to know Perl, I suggest you to contribute to VNDB directly (reference: [vndb/lib/VNWeb/Misc/Feeds.pm - yorhel/vndb](https://code.blicky.net/yorhel/vndb/src/branch/master/lib/VNWeb/Misc/Feeds.pm)) so no third party tool is needed. That being said, any contribution is appreciated, either to VNDB or this repository.

## Acknowledgement

- Inspired by [SteamWishlistCalendar](https://github.com/icue/SteamWishlistCalendar), which I highly recommend in favor of email notifications
- [VNDB Steam Enhancer](https://greasyfork.org/en/scripts/456166-vndb-steam-enhancer/code) is another learning source for interacting with VNDB API
- Thanks to all VNDB contributors & editors for making such a great site available
