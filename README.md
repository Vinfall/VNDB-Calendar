# VNDB Release Calendar

中文介绍请看 [README_zh-Hans](README_zh-Hans.md)

## Intro

This tiny tool allows you to create a calendar of [VNDB](https://vndb.org) [upcoming releases](https://vndb.org/r?f=01731;o=a;s=released). Everything is supposed to be automated via GitHub Actions after initial setup. If you choose to publish the `ICS` file, you can just subscribe it in any calendar app that supports iCalendar. A highly customized example including ja, zh-Hans & zh-Hant releases (not very suitable for en readers) is avaialable [here](https://raw.githubusercontent.com/Vinfall/VNDB-RelCalendar/main/output/vndb-rel-calendar.ics).

## Why

For now VNDB only offers RSS for *Recent Changes*, but not *Upcoming Releases* or *Just Released*. There are multiple previous discussions about that but I don't think Yorhel is going to do that any time soon.

This is created as a workaround (just in ICS rather than RSS) for personal use and serves as an extended practice of my blog post [iCalendar (ICS) 的养成方式](https://blog.vinfall.com/posts/2023/12/ics/) (written in Chinese).

## Usage

The results should be similar to the one you would see in [this release query on VNDB](https://vndb.org/r?f=0672171_4YsVe132gja2wzh_dHans-2wzh_dHant-N48721gwcomplete-N480281UJ81Xkx), except that I expand the release window 14 days earlier to avoid missing VNs.

To customize the query, run the script with optional parameters:
- `python vndb-calendar.py -f {customized_compact_filter} -p {max_page} -t {shift_time}`
- Example of generic filters for en & ja upcoming releases: `python vndb-calendar.py -f "0572171_4YsVe122gen2gjaN48721gwcomplete-" -t 0`
- `-f` or `--filter`: your custom [compact filters](https://api.vndb.org/kana#filters), by default it would use my personalized one
- `-p` or `--max-page`: maximum pages of query results, by default it will be `2`
- `-t` or `--shift-time`: show *new* releases X days ago, it's really upcoming release if set to `0`, by default it will be `14`

## Todo

- [x] Remove redundant releases of the same VN
- [x] Declutter common release variate titles like `ダウンロード版` and `DLカード版`
- [x] Better handling of incomplete date like `2026` and `2024-02`
- [x] Filter out BLG/Otome game & other tags I wish to avoid
- [x] Add filters arguments (you can use [compact filters](https://api.vndb.org/kana#filters) to quickly customize the results)
- [ ] Generic filter for en & ja release (probably in a tagged automated release, low priority as DIY instructions are given in [#Usage](#usage))
- [ ] Find out why many filters would make responses 400, and add more info in calendar events afterwards
- [ ] User wishlist, just like SteamWishlistCalendar (low priority as I don't use VNDB this way)
- [ ] Add external links (Getchu/DMM/DLsite/Steam/Official website etc.) to event description (maybe not possible w/o refactoring)

## Contribution

If you happen to know Perl, I suggest you to contribute to VNDB directly (reference: [vndb/lib/VNWeb/Misc/Feeds.pm - yorhel/vndb](https://code.blicky.net/yorhel/vndb/src/branch/master/lib/VNWeb/Misc/Feeds.pm)) so no third party tool is needed. That being said, any contribution is appreciated, either to VNDB or this repository.

## Acknowledgement

- Inspired by [SteamWishlistCalendar](https://github.com/icue/SteamWishlistCalendar), which I highly recommend in favor of email notifications
- [VNDB Steam Enhancer](https://greasyfork.org/en/scripts/456166-vndb-steam-enhancer/code) is another learning source for interacting with VNDB API
- Thanks to all VNDB contributors & editors for making such a great site available
