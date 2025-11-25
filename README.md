# VNDB Calendar

[![Build][build]][build-ci] [![Release][release]][release-ci] [![Test][test]][test-ci]

中文介绍请看 [README_zh-Hans](README_zh-Hans.md)

## Intro

For now VNDB only offers RSS for *Recent Changes*, but not *Upcoming Releases* or *Just Released*.
This tool allows you to create a calendar of [VNDB](https://vndb.org) [upcoming releases][released],
    and serves as an extension of my blog post [iCalendar (ICS) 的养成方式][ics] (written in Chinese).

After initial setup, everything would be automatically updated.
If you choose to publish the `ICS` file, you can subscribe it in any calendar app that supports iCalendar.

These example calendars are provided for quick test, if they already satisfy you, no need to read further:
- [en][en]: upcoming en & ja releases
- [enpatch][enpatch]: unofficial en localization/content restoration patches released in 2025

## Setup

If you want a more personalized calendar, you may want to fork the repo and customize your query.
More details about parameter are available in [USAGE](USAGE.md).

Minimal setup workflow:
1. Head to [Browse releases][vndb] page on VNDB, customize your filters here and copy the *filters*
   - For example, the URL for [enpatch][enpatch] query would be something like this:
     - `https://vndb.org/r?q=&o=a&s=title&f=052genNg1174172_0ceJ4N483hen`
     - `https://vndb.org/r?f=052genNg1174172_0ceJ4N483hen&o=a&s=released`
   - The *filters* here are `052genNg1174172_0ceJ4N483hen`, which is needed later
2. Fork the repo
3. Replace `default_filters` in [vndb_calendar.py](vndb_calendar.py) with your filters here

    ```python
    # fmt: on

    # ↓↓↓ change this line ↓↓↓
    default_filters = "052genNg1174172_0ceJ4N483hen"
    # ↑↑↑ change this line ↑↑↑

    default_data = {
        ...
    }
    ```

4. Get your personalized calendar at [output/vndb-calendar.ics][custom] (change your username in URL)

## Contrib

Any contribution is appreciated!

If you happen to know Perl, you'd better contribute to VNDB directly (reference: [vndb/lib/VNWeb/Misc/Feeds.pm - yorhel/vndb][Feeds.pm]) to get rid of third party tool.

## Acknowledgement

- Inspired by [SteamWishlistCalendar][swc], which I highly recommend in favor of email notifications
- [VNDB Steam Enhancer][vndb-steam-enhancer] is another learning source for interacting with VNDB API
- Thanks to all VNDB contributors & editors for making such a great site available

[build]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/custom.yml/badge.svg
[build-ci]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/custom.yml
[release]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/release.yml/badge.svg
[release-ci]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/release.yml
[test]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/test.yml/badge.svg
[test-ci]: https://github.com/Vinfall/VNDB-Calendar/actions/workflows/test.yml
[released]: https://vndb.org/r?f=01731&o=a&s=released
[en]: https://github.com/Vinfall/VNDB-Calendar/releases/download/en/vndb-calendar.ics
[enpatch]: https://github.com/Vinfall/VNDB-Calendar/releases/download/enpatch/vndb-calendar.ics
[ics]: https://blog.vinfall.com/posts/2023/12/ics/
[Feeds.pm]: https://code.blicky.net/yorhel/vndb/src/branch/master/lib/VNWeb/Misc/Feeds.pm
[swc]: https://github.com/icue/SteamWishlistCalendar
[vndb-steam-enhancer]: https://greasyfork.org/en/scripts/456166-vndb-steam-enhancer/code
[custom]: https://github.com/yourusername/VNDB-Calendar/raw/refs/heads/main/output/vndb-calendar.ics
[vndb]: https://vndb.org/r
