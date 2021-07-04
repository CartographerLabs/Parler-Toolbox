"""
A script to be used on the output of the 'body-aggregator' script. This script iterates through all Parler post bodies]
looking for a root (or series of root) hashtags. Hashtags in the posts containing this root hashtag are stored until
all messages have been processed. The process is then continued with this new list of hashtags. The goal is to create a
corpus

Params:
depth_range: Used to define the amount of iterations that will be performed
max_per_depth: used to define the amount of hashtags each run that will be aggregated

The goal is to bootstrap far-right hashtags that will be used to split the dataset into a far-right corpus, and non-far-right
corpus.
"""

import csv
import re

import easy_db

dict_of_extreamist_messages = {}
dict_of_non_extreamist_messages = {}

depth_range = 10000
max_per_depth = 500

used_hastags = []
search_hashtags = ["wwg1wga","proudboys", "patriotsawakened", "DigitalArmy", "DigitalWarriors",
                                "itookanoath", "weareallproud",
                                "thestormisuponus", "digitalsoldiers", "fightback", "fightfortrump",
                                "qarmy", "qanons", "newqdrop", "qcrumbs", "wakeupamerica", "takebackamerica",
                                "qanonpatriots"]

collected_hashtags = {}

messages = []

print("Loading DB")
db = easy_db.DataBase(r'parler-messages.db')
posts = db.pull('parler_messages')

for post in posts:
    messages.append(post["body"])

length_of_data = len(messages)

# Loops for a max depth
for depth in range(0, depth_range):
    collected_hashtags = {}

    search_hastag_count = 0
    # Loops through all hastags to be searched for
    for search_hashtag in search_hashtags:
        used_hastags.append(search_hashtag)

        # Write to file as we go
        output_file = open("output-hashtags.txt", "w", encoding="utf8")
        for hastag in used_hastags:
            output_file.write(hastag + "\n")
        output_file.close()

        search_hastag_count = search_hastag_count + 1
        # Loop through all rows of messages looking for the hastag that's being searched for
        message_count = 0

        # Loops through all messages
        for message in messages:
            message_count = message_count + 1
            print(
                "In depth {} of max {}. Searching hashtag {} - count {} of {}. Message row {} of {}. Found hastags: {}".format(
                    depth, depth_range, search_hashtag, search_hastag_count, len(search_hashtags), message_count,
                    length_of_data, len(used_hastags)
                ))

            if search_hashtag.lower() in message.lower():
                # Strip the found hashtag
                message = message.lower().replace("#" + search_hashtag, "")
                message = message.lower().replace(search_hashtag, "")

                # Get all other hashtags
                hashtags = re.findall(r"#(\w+)", message)

                for hashtag in hashtags:
                    # If the hastag is already accounted for add one to the count
                    if hashtag in collected_hashtags:
                        collected_hashtags[hashtag] = collected_hashtags[hashtag] + 1
                    else:
                        collected_hashtags[hashtag] = 1

    # Sort all collected hastags in most common order
    # todo this is lowest to highest?
    sorted(collected_hashtags, key=collected_hashtags.get, reverse=True)
    # collected_hashtags = {k: v for k, v in sorted(collected_hashtags.items(), key=lambda item: item[1])}
    # Get the top ten percent
    number_of_hastags = len(collected_hashtags)
    top_1_percent = int(number_of_hastags / 10)

    if top_1_percent < 1:
        top_1_percent = 1

    if top_1_percent > max_per_depth:
        top_1_percent = max_per_depth

    selected_hastags = list(collected_hashtags.keys())
    selected_hastags = selected_hastags[0:top_1_percent]

    # check that we're not iterating over the same hastags again
    search_hashtags = []
    for hashtag in selected_hastags:
        if hashtag not in used_hastags:
            # Add hastags to list for crawl
            search_hashtags.append(hashtag.strip("#"))

# Write to file when completed
output_file = open("output-hashtags.txt", "w", encoding="utf8")
for hastag in used_hastags:
    output_file.write(hastag + "\n")
output_file.close()
