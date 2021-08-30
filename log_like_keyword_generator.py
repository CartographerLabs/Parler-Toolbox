"""As the Hashtag Bootstrapping provides a large amount of hashtags that aren’t necessarily related to far-right
extremism or violent far-right extremism other approaches can be used for generating these keywords. Utilizing the
script from Mikesuhan this script requires that you have a CSV file with Parler data in and that some of that data
has been marked up with TRUE and FALSE (for example TRUE if the message contains far-right extremism). Make sure to
set the CSV field accordingly in the script. Then this script compares the frequencies of tokens or ngrams in the
TRUE and FALSE corpus, rank ordering the output by the log likelihood values of the corpus. Then the top x keywords
found to have the highest log likelihood between the TRUE and FALSE corpuses will be saved to an output file (in a
similar manner to the bootstrapping script. Make sure to set the ``` ORIGINAL_CSV_TO_READ_LOCATION```,
``` NUMBER_OF_TOP_KEYWORDS_TO_STORE```, and ``` DESTINATION_FILE_NAME```. As well as the variables used for
retrieving data from the CSV file: ``` username = row[0]```, ``` message = row[2]```, and ``` is_extremist = row[
3]```. """

import csv
import re

from keyness import log_likelihood
from nltk.corpus import stopwords

list_of_extreamist_messages = []
list_of_non_extreamist_messages = []
not_labelled = []
# A list of strings that should be ignored if they come up in the log-like keywords
deny_list_words = ["accosted", "antifa", "nadler", "freedoms", "random", "left", "millions", "veterans", "belongs",
                   "eternal", "setup", "greatgrandkids", "lays", "creepyjoebiden", "georgesoros", "news", "steps",
                   "oprahwinfrey", "billclinton", "iranian", "must", "theyll", "expect", "o", "well", "happens", "wh",
                   "an", "eventually", "w", "nwo", "man", "never", "foot", "ensure", "and", "un", "five", "later",
                   "soon", "copy", "rather", "jill", "doi", "shie", "embraced", "an", "un", "and", "well", "water",
                   "tgat", "soon", "doi"]

# TODO Set these variables accordingly
ORIGINAL_CSV_TO_READ_LOCATION = 'joint-data.csv'
NUMBER_OF_TOP_KEYWORDS_TO_STORE = 25
DESTINATION_FILE_NAME = "top-violent-extremist-keyworks.txt"


class message_object():
    """
    A class used to store message data
    """
    original_message = None
    message_to_process = None
    username = None
    follow_ration = None
    post_ration = None

    def __init__(self, original_message, username, follow_ration="", post_ration=""):
        self.original_message = original_message
        self.message_to_process = original_message
        self.username = username
        self.follow_ration = follow_ration
        self.post_ration = post_ration


def remove_url(txt):
    "Removes URLs from a string"
    return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())


def clean_list_of_messages(list_to_process):
    """Takes a message object, cleans the message and assigns the message to process variable with it """
    new_list = []

    for message_object in list_to_process:
        message = message_object.original_message
        message = remove_url(message)
        words = ""
        for word in message.split(" "):

            word = word.replace("#", "")

            if word.startswith("@"):
                continue

            if word in deny_list_words:
                continue

            if word not in stopwords.words('english'):
                words = words + word.lower() + " "

        message_object.message_to_process = words


def get_words_from_list(list_to_process):
    """
    Takes a list of strings and returns a string seperated by spaces of each word in that list
    """
    words = ""
    for message in list_to_process:
        message = message.original_message
        message = remove_url(message)
        for word in message.split(" "):

            word = word.replace("#", "")

            if word.startswith("@"):
                continue

            if word not in stopwords.words('english'):
                words = words + (word.lower()) + " "

    return words


# Reads the csv file that contains the marked up data. Here field 0 is the username, 2 is the message, and 3 is the
# marked up field of is violent extremist
with open(ORIGINAL_CSV_TO_READ_LOCATION) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:

        username = row[0]
        message = row[2]
        is_extremist = row[3]

        message = message_object(message, username)

        # Assigns message to appropriate list based on labell
        if is_extremist == 'TRUE':
            is_extremist = True
        elif is_extremist == 'FALSE':
            is_extremist = False
        else:
            not_labelled.append(message)

        if is_extremist == True:
            list_of_extreamist_messages.append(message)
        elif is_extremist == False:
            list_of_non_extreamist_messages.append(message)

# Cleans the extremist and non extremist lists
clean_list_of_messages(list_of_extreamist_messages)
clean_list_of_messages(list_of_non_extreamist_messages)

list_of_just_extremist_messages = []

# get list of words from extremist and non extremist lists for the log liklihood. Takes time.
for message in list_of_extreamist_messages:
    list_of_just_extremist_messages.append(message.message_to_process.split(" "))

list_of_just_non_extremist_messages = []

for message in list_of_non_extreamist_messages:
    list_of_just_non_extremist_messages.append(message.message_to_process.split(" "))

log_Like = log_likelihood(list_of_just_extremist_messages, list_of_just_non_extremist_messages)

# Get Top Keywords, that will be used for splitting the dataset
number_of_top_keywords = NUMBER_OF_TOP_KEYWORDS_TO_STORE
iterator = 0
top_keywords = []
for keyword in log_Like:
    keyword = keyword[0]

    if keyword not in deny_list_words:
        top_keywords.append(keyword)
        iterator = iterator + 1

    if iterator >= number_of_top_keywords:
        break

# Write log-like to file
keywords_file = open(DESTINATION_FILE_NAME, "w")

for keyword in top_keywords:
    keywords_file.write(keyword + "\n")
