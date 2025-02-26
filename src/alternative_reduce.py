#!/usr/bin/env python3

# command line args

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_paths',nargs='+',required=True)
parser.add_argument('--keys',nargs='+',required=True)
parser.add_argument('--output_path',required=True)
args = parser.parse_args()

# imports
import os
import json
import pandas as pd
from collections import Counter,defaultdict
import matplotlib.pyplot as plt

# load each of the lang input paths
total = defaultdict(lambda: Counter())
date = pd.to_datetime('2020-01-01')
for path in args.input_paths:
    with open(path) as f:
        tmp = json.load(f)
        for k in tmp:
            count = sum(tmp[k].values())
            total[date.strftime('%Y-%m-%d')][k] = count
        date += pd.Timedelta(days=1)

dates = pd.to_datetime(sorted(total.keys()))

for hashtag in args.keys:
    counts = [total[date.strftime('%Y-%m-%d')].get(hashtag, 0) for date in dates]
    print(f"Counts for {hashtag}: {counts}")

for hashtag in args.keys:
    counts = [total[date.strftime('%Y-%m-%d')].get(hashtag, 0) for date in dates]
    plt.plot(dates, counts, marker='o', linestyle='-', label=hashtag)

plt.xlabel('Date')
plt.ylabel('Count')
plt.title("Hashtag Trends Over Time")
plt.legend()
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.savefig(args.output_path,bbox_inches="tight")
