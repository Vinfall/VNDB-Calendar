# Usage

## Release Calendar

To customize the query, run [`vndb_calendar.py`](vndb_calendar.py) with optional parameters:
- `python vndb_calendar.py -f {customized_compact_filter} -p {max_page} -t {shift_time} -d {1 or 0} -b {0 or 1}`
- Example of generic filters for en & ja upcoming releases with description: `python vndb-calendar.py -f "0572171_4YsVe122gen2gjaN48721gwcomplete-" -t 0 -d 1 -b 0`
- `-f` or `--filter`: your custom [compact filters](https://api.vndb.org/kana#filters), by default it would use my personalized one
- `-p` or `--max-page`: maximum pages of query results, by default it will be `2`
- `-t` or `--shift-time`: show *new* releases X days ago, it's really upcoming release if set to `0`, by default it will be `14`
- `-d`, `--description` or `--intro`: add VN description to calendar event, bool type (only `0`/`1` is supported), by default `0`/`False`
- `-b`, `--beta` or `--partial`: show partial releases in query results, e.g. multiple chapters

## Wishlist Calendar

This is basically an inferior version of release calendar with the focus on user wishlist.

Nothing to customize actually, simply run [`wishlist.py`](wishlist.py):
- `python wishlist.py -u "{uid}" -p {max_page}`
- Example of Yorhel's wishlist: `python wishlist.py -u "u2"`
- `-u` or `--user`: user id **with** 'u', e.g. `u2`
- `-p` or `--max-page`: maximum pages of query results, by default it will be `1`. As wishlist is fetched reversely, newest items come first. Each page has 100 items, so 1 page is usually suffecient if you use calendar only for upcoming releases.

> [!NOTE]
> `wishlist.py` assumes you use the default `wishlist` label and have not set it to private.
> If you prefer to use another default label or your custom labels to generate calendar,
> use attached one-liner in the script to determine the label id and change `default_filters`.
