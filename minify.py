#!/usr/bin/env python3

import csv
import os

INPUT = "output/vndb-release.txt"
OUTPUT = "output/vndb.csv"

with open(INPUT, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f, delimiter=";")
    best = {}

    for row in reader:
        vid = row["vid"]
        # keep vid row with the earliest released
        if vid not in best or row["released"] < best[vid]["released"]:
            best[vid] = row

with open(OUTPUT, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow(["vid", "title", "released"])

    for row in best.values():
        writer.writerow([row["vid"], row["title"], row["released"]])

os.remove(INPUT)
