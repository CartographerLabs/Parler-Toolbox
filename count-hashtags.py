"""
This tooling iterates through the Parler post Json files (set in the ```folder_of_data``` variable)
and counts all occurances of the hashtags in the  ```output-hashtags.txt```file (set in the ```output_file``` variable).
This tooling creates a sorted JSON file of all occurances of the number of times each hashtag occured
(called ```hashtag-count.json```).
"""

import csv
import csv
import gc
import json
import json
import os
import re
from datetime import date
from datetime import datetime

cached_usernames = {}

folder_of_data = r"parler_data"

list_of_hashtags = []
output_file = open("output-hashtags.txt", "r", encoding="utf8")
for hastag in output_file.readlines():
    list_of_hashtags.append(hastag.strip("\n"))
output_file.close()


def get_all_files_in_a_folder(directory):
    list_of_files = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json") or filename.endswith(".ndjson"):
            list_of_files.append(os.path.join(directory, filename))
    return list_of_files


def process_data():
    all_data_files = get_all_files_in_a_folder(folder_of_data)

    number_of_actual_prcoessed = 0
    file_count = 0

    date_dict = {}
    dict_of_hashtag_count = {}
    number_of_data_files = len(all_data_files)
    for file in all_data_files:
        file_count = file_count + 1
        json_entry_count = 0
        print("Opening file {}".format(file))
        with open(file, encoding='utf8', newline='') as json_file:
            list_of_data = []
            for line in json_file:
                list_of_data.append(json.loads(line))

            number_of_data = len(list_of_data)
            message_count = 0
            for data in list_of_data:
                json_entry_count = json_entry_count + 1

                message_count = message_count + 1

                try:
                    message = data["body"]
                except:
                    print("No body, skipping")
                    continue

                if message == "":
                    print("No body, skipping")
                    continue

                # Loops through all hastags to be searched for
                search_hastag_count = 0
                for search_hashtag in list_of_hashtags:

                    search_hastag_count = search_hastag_count + 1
                    # Loop through all rows of messages looking for the hastag that's being searched for

                    print(
                        "In file {} of {}. Hashtag '{}' of Hashtags '{}', searched in message '{}' of messages '{}'".format(
                            file_count, number_of_data_files,
                            search_hastag_count, len(list_of_hashtags), message_count, number_of_data))

                    if search_hashtag.lower() in message.lower():

                        if search_hashtag.lower() in dict_of_hashtag_count.keys():
                            dict_of_hashtag_count[search_hashtag.lower()] = dict_of_hashtag_count[
                                                                                search_hashtag.lower()] + 1
                        else:
                            dict_of_hashtag_count[search_hashtag.lower()] = 1

                # Write to file when completed
                sorted(dict_of_hashtag_count, key=dict_of_hashtag_count.get, reverse=True)
                output_file = open("hashtag-count.json", "w", encoding="utf8")
                json.dump(dict_of_hashtag_count, output_file)

        gc.collect()

    sorted(dict_of_hashtag_count, key=dict_of_hashtag_count.get, reverse=True)
    with open("hashtag-count.json", "w") as outfile:
        json.dump(date_dict, outfile)


process_data()
