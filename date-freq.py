"""
This tooling iterates over the Parler posts and identifies the frequency of extreamist
v.s. non-extreamist using the hashtags previously obtained (where if 10% of a post or
more is made up of the hashtags it's deemed as extreamist). This tooling takes the name
of the folder where the Parler Json posts are (via the ```folder_of_data``` variable),
and the previously created list of hashtags via the ```output_file``` variable. This
tooling could easily be used to distinguish between other factors. This tooling creates
a JSON file called ```date-freq.json``` which contains the frequencies.
"""

import csv
import gc
import json
import os
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
            for data in list_of_data:
                json_entry_count = json_entry_count + 1

                try:
                    body = data["body"]
                except:
                    print("No body, skipping")
                    continue

                if body == "":
                    print("No body, skipping")
                    continue

                created_date = data["createdAt"]  # "20200723195913"
                # example: '2020-1114182509'
                year = int(created_date[0:4])
                month = int(created_date[4:6])
                day = int(created_date[6:8])
                created_date = date(year, month, day)

                is_extreamist = False
                body_lines = body.split(" ")
                length_of_body = len(body_lines)
                percentage_val = int(length_of_body / 50)
                found_extreamist_words = 0
                found_words = []
                for word in body_lines:

                    # print("list of {} against {}".format(len(list_of_hashtags), body))
                    if word.replace("#", "") in list_of_hashtags:
                        found_extreamist_words = found_extreamist_words + 1
                        found_words.append(word)

                        # 10 percent of the post should contain extreamist words
                        if found_extreamist_words >= percentage_val and found_extreamist_words != 0:
                            print("Post is extreamist, extreamist words found: {}. from words {}".format(
                                found_extreamist_words, found_words))
                            is_extreamist = True
                            break

                key = str(created_date.year) + "-" + str(created_date.month)
                if key in date_dict:
                    date_dict[key]["total"] = date_dict[key]["total"] + 1
                    if is_extreamist:
                        date_dict[key]["extreamist"] = date_dict[key]["extreamist"] + 1
                    else:
                        date_dict[key]["non-extreamist"] = date_dict[key]["non-extreamist"] + 1

                else:
                    if is_extreamist:
                        date_dict[key] = {"total": 1, "extreamist": 1, "non-extreamist": 0}
                    else:
                        date_dict[key] = {"total": 1, "extreamist": 0, "non-extreamist": 1}

                print(
                    "Processed entry in file {} of {}, json entry {} of {}. Post was extreamist {} - data for same month {}: {} ".format(
                        file_count, number_of_data_files, json_entry_count, number_of_data, is_extreamist, key,
                        date_dict[key]))

        gc.collect()

    with open("date-freq.json", "w") as outfile:
        json.dump(date_dict, outfile)


process_data()
