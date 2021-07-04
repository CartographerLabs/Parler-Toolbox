"""
Once provided with the name of the create Parler username database
(via the ```user_db``` variable) and the folder of parler posts (via the ```folder_of_data```)
variable, this tooling will process all Parler posts and add them to a databse called
```parler-messages.db``` with a single table called ```parler_messages``` and fields:
username, body, follow_freq, post_freq, and Time. This tooling could be extended to
include additional fields from the Parler data.
"""

import csv
import gc
import json
import os
from datetime import date
from datetime import datetime

import easy_db

cached_usernames = {}
user_db = easy_db.DataBase(r'parler-data.db')

folder_of_data = r"parler_data"


def find_user_data(username):
    result = user_db.pull_where('parler_users', "username = '{}'".format(username))

    if result == []:
        raise Exception("Couldn't find a username entry for user {}".format(username))

    if len(result) > 1:
        raise Exception("The datase returned more than one entry for the user {}. {}".format(username, result))

    return result[0]


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

                body = data["body"]

                if body == "":
                    print("No body, skipping")
                    continue

                username = data["username"]

                print(
                    "Processing user {}, in file {} of {}, json entry {} of {}. Number of actual processed users {}".format(
                        username, file_count, number_of_data_files, json_entry_count, number_of_data,
                        number_of_actual_prcoessed))

                try:
                    username_dict = find_user_data(username)
                except:
                    print("Couldn't find username {}".format(username))
                    continue

                post_frequency = username_dict["post_freq"]
                follow_ratio = username_dict["follow_freq"]
                created_date = data["createdAtformatted"]

                all_db.append('parler_messages',
                              {"username": username, "body": body, "follow_freq": follow_ratio,
                               "post_freq": post_frequency, "Time": created_date})
                number_of_actual_prcoessed = number_of_actual_prcoessed + 1
        gc.collect()


all_db = easy_db.DataBase(r'parler-messages.db')
all_db.create_table('parler_messages',
                    {"username": "TEXT", "body": "TEXT", "follow_freq": "INTEGER", "post_freq": "INTEGER",
                     "Time": "TEXT"},
                    force_overwrite=True)
process_data()
