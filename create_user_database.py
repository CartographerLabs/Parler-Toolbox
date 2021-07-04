"""
Once updated the ```user_folder``` variable to a folder containing all of the Parler users,
this script will iterate through all users and create a database file with the table ```parler_users```.
Inside of this table all users will be aggregated with the following fields:
```username```, ```follow_freq```, ```post_freq```. This tooling could be extended to include additional
fields from the Parler data.
"""

import json
import os
from datetime import date
import easy_db

user_folder = r"parler_users (1)"
db = None


def get_all_files_in_a_folder(directory):
    list_of_files = []
    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.endswith(".json") or filename.endswith(".ndjson"):
            list_of_files.append(os.path.join(directory, filename))
    return list_of_files


def find_user_data():
    all_username_files = get_all_files_in_a_folder(user_folder)

    number_of_files = len(all_username_files)
    file_count = 0
    for file in all_username_files:
        file_count = file_count + 1
        print("Opened file {}".format(file))
        with open(file, encoding='utf-8', newline='') as data_file:
            list_of_data = []
            for line in data_file:
                list_of_data.append(json.loads(line))

            length = len(list_of_data)
            count = 0
            for username_dict in list_of_data:

                try:

                    count = count + 1

                    username = username_dict["username"]

                    print("Processing user {}, count {} of {}. In file {} of {}".format(username, count, length,
                                                                                        file_count, number_of_files))

                    being_followed_count = username_dict["user_followers"]
                    following_count = username_dict["user_following"]
                    joined_date = username_dict["joined"]
                    last_seen = username_dict["lastseents"]

                    # example: '2020-1114182509'
                    year = int(joined_date[0:4])
                    month = int(joined_date[4:6])
                    day = int(joined_date[6:8])
                    start_date = date(year, month, day)
                    # example:  "2020-12-23
                    last_seen_date = date(int(last_seen[0:4]), int(last_seen[5:7]), int(last_seen[8:10]))
                    delta = last_seen_date - start_date
                    total_active_days = delta.days
                    number_of_posts = username_dict["posts"]

                    # Minimum day alive is 1
                    if total_active_days == 0:
                        total_active_days = 1

                    post_frequency = number_of_posts / total_active_days
                    follow_ratio = being_followed_count / following_count

                    db.append('parler_users',
                              {"username": username, "follow_freq": follow_ratio, "post_freq": post_frequency})

                except:
                    pass


db = easy_db.DataBase('parler-data.db')
db.create_table('parler_users', {"username": "TEXT", "follow_freq": "INTEGER", "post_freq": "INTEGER"},
                force_overwrite=True)
find_user_data()
