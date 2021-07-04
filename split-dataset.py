"""
A script to be used on the full corpus and a list of far-right hashtags, provided by the output of hashtag-bootstrapping.py.
This script will create two sub-corpuses, one which only includes posts containing the far-right hashtags and one of no
posts of far-right hashtags.
"""

import csv
import json
import random

import easy_db

keywords_location = r"output-hashtags.txt"

list_of_extreamist_messages = []
list_of_non_extreamist_messages = []

# Read keywords from keywords file
keywords_file = open(keywords_location, "r")
extreamist_keywords = keywords_file.read().splitlines()
keywords_file.close()

print("Loading DB")
db = easy_db.DataBase(r'parler-messages.db')
posts = db.pull('parler_messages')


def percentage(percent, whole):
    return (percent * whole) / 100.0


def get_frequency():
    with open(r"date-freq.json") as jsonFile:
        date_ranges = json.load(jsonFile)
        jsonFile.close()

    list_of_extremism_frequency = []
    list_of_non_extremism_frequency = []
    for key in date_ranges.keys():
        entry = date_ranges[key]
        total = entry["total"]

        extreamist_posts = entry["extreamist"]
        frequency = extreamist_posts / total
        list_of_extremism_frequency.append(frequency)

        non_extreamist_posts = entry["non-extreamist"]
        frequency = non_extreamist_posts / total
        list_of_non_extremism_frequency.append(frequency)

    average_ext_frequency = sum(list_of_extremism_frequency) / len(list_of_extremism_frequency)
    average_ext_frequency = average_ext_frequency
    average_ext_frequency = average_ext_frequency * 100

    average_non_ext_frequency = sum(list_of_non_extremism_frequency) / len(list_of_non_extremism_frequency)
    average_non_ext_frequency = average_non_ext_frequency
    average_non_ext_frequency = average_non_ext_frequency * 100

    return {"extreamist_freq": average_ext_frequency, "non_extreamist_freq": average_non_ext_frequency}


frequencies = get_frequency()
extreamist_freq = frequencies["extreamist_freq"]
non_extreamist_freq = frequencies["non_extreamist_freq"]

number_of_entries = len(posts)

random.shuffle(posts)

count = 0
for post in posts:

    count = count + 1

    is_extreamist = False

    name = post["username"]
    body = post["body"]
    follow_freq = post["follow_freq"]
    post_freq = post["post_freq"]
    time = post["Time"]

    body_lines = body.split(" ")
    length_of_body = len(body_lines)
    percentage_val = int(length_of_body / 50)

    found_keyword = ''
    random.shuffle(extreamist_keywords)
    found_extreamist_words = 0
    found_keywords = []
    for word in body_lines:
        word = word.replace("#", "")
        if word.lower() in extreamist_keywords:
            found_extreamist_words = found_extreamist_words + 1
            found_keywords.append(word)

    # 10 percent of the post should contain extreamist words
    if found_extreamist_words >= percentage_val and found_extreamist_words != 0:
        is_extreamist = True

    if is_extreamist:
        print("Found extreamist message - {} of {}. Via keyword {}".format(count, number_of_entries, found_keywords))
        list_of_extreamist_messages.append(
            {"username": name, "timestamp": time, "message": body, "follow_freq": follow_freq, "post_freq": post_freq})
    else:
        list_of_non_extreamist_messages.append(
            {"username": name, "timestamp": time, "message": body, "follow_freq": follow_freq, "post_freq": post_freq})

print("Finished with total number {} extreamist messages and {} non-extreamist, with total of {}".format(
    len(list_of_extreamist_messages), len(list_of_non_extreamist_messages),
    len(list_of_extreamist_messages) + len(list_of_non_extreamist_messages)
))

# get total number of posts
# get expected ration of each of the new number of data

total_number_of_posts = len(list_of_extreamist_messages) + len(list_of_extreamist_messages)

number_of_expected_extreamist_posts = int(percentage(extreamist_freq, (total_number_of_posts)))
list_of_extreamist_messages = list_of_extreamist_messages[0:number_of_expected_extreamist_posts:]

number_of_expected_non_extreamist_posts = int(percentage(non_extreamist_freq, total_number_of_posts))
list_of_non_extreamist_messages = list_of_non_extreamist_messages[0:number_of_expected_non_extreamist_posts]

# Write extreamist data
with open('extreamist-messages.csv', 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file,
                        fieldnames=list_of_extreamist_messages[0].keys(),
                        )
    fc.writeheader()
    fc.writerows(list_of_extreamist_messages)

# Write non-extreamist data
with open('non-extreamist-messages.csv', 'w', encoding='utf8', newline='') as output_file:
    fc = csv.DictWriter(output_file,
                        fieldnames=list_of_non_extreamist_messages[0].keys(),
                        )
    fc.writeheader()
    fc.writerows(list_of_non_extreamist_messages)
