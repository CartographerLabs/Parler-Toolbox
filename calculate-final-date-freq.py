"""
An additional piece of tooling has been created that reads the aformentioned
JSON file and returns the total percentage frequency of each category of post.
This script must be provided with the path to the ```date-freq.json``` file.
"""

import json

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

print(
    "The average frequency of extreamist posts per month on Parler is: '{}%', with average non-extreamist: '{}%'".format(
        average_ext_frequency, average_non_ext_frequency))
