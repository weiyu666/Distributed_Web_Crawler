import json
import requests
import queue
import sys
import urllib
import os
import urllib.request
from collections import Counter


class MovieData:

    __movie_list, count = list(), ""

    def update(self, is_use_last=False):
        if not is_use_last:
            print("Updating...Please wait...")
            t = requests.get(
                "http://www.artrix.tech/doubanspider/result.txt").text
            f = open("temp", mode="w", encoding="utf-8")
            f.write(t)
            file = open("temp", mode="r", encoding="utf-8")
            movie_count = 0
            all_list = list()
        else:
            if os.path.exists("temp"):
                print("Using file cache...")
                file = open("temp", mode="r", encoding="utf-8")
                movie_count = 0
                all_list = list()
            else:
                print("Updating...Please wait...")
                t = requests.get(
                    "http://www.artrix.tech/doubanspider/result.txt").text
                f = open("temp", mode="w", encoding="utf-8")
                f.write(t)
                file = open("temp", mode="r", encoding="utf-8")
                movie_count = 0
                all_list = list()

        while True:
            line = file.readline()
            if line == "":
                break
            if not line == " ":
                try:
                    all_list.append(json.loads(line))
                    movie_count += 1
                except:
                    pass
        print("finished")
        self.__movie_list, self.count = all_list, movie_count

    def request_all_movie(self, keyword):

        have_in_once = False
        have_in_all = False
        return_list = list()

        for line in self.__movie_list:

            have_in_once = False
            key_list = list()

            # search all keys and find the command.
            for key in line:
                key_list.append(key)
            for keys in key_list:
                try:
                    # if this row is an iterable list:
                    if isinstance(line[keys], list):
                        for sub_key in line[keys]:
                            if keyword in str(sub_key) or keyword in str(
                                    sub_key).lower():
                                if not have_in_once:
                                    return_list.append(line)
                                    have_in_once = True
                                    have_in_all = True
                    else:
                        if keyword in str(
                                line[keys]) or keyword in str(
                                line[keys]).lower():
                            if not have_in_once:
                                return_list.append(line)
                                have_in_once = True
                                have_in_all = True
                except:
                    pass
        # no result
        if not have_in_all:
            return False
        else:
            return return_list

movie = MovieData()
movie.update(True)

while True:
    try:
        print(
            "What are you going to do? \"Search:[movie name]\" can search , \"update:\" can update datas.")
        command = input()
        if "Search:" in command:
            # search by tag
            if " -tag" in command:
                command_key = str(command).replace(
                    "Search:", "").replace(
                    " -tag", "")
                target_movies = movie.request_all_movie(command_key)
                if target_movies:
                    all_tags = Counter()
                    index = 0
                    for new_movie in target_movies:
                        key_list = list()
                        for key in new_movie:
                            key_list.append(key)
                        for sub_data in key_list:
                            # Calc the tag data.
                            if sub_data == "tags":
                                for tag in new_movie[sub_data]:
                                    all_tags[tag] += 1
                        print("[%s]:%s" % (index, new_movie["name"]))
                        index += 1
                    print("------------------------------------------------")
                    tag_list = list()
                    for tags in all_tags:
                        tag_list.append(tags)
                    print("all Tags（from high frequency to low):%s" % tag_list)
                    print("------------------------------------------------")
                else:
                    print("No result!")

            # if no attached argument:
            elif " -tag" not in command and " -index" in command:
                index_command = ""
                for i in range(str(command).find(" -index"), len(command)):
                    index_command += command[i]
                command_key = str(command).replace(
                    "Search:", "").replace(index_command, "")
                index_command = index_command.replace(" -index ", "")
                target_movies = movie.request_all_movie(command_key)
                if target_movies:
                    new_movie = target_movies[int(index_command)]
                    key_list = list()
                    for key in new_movie:
                        key_list.append(key)
                    for sub_data in key_list:
                        print("%s : %s" % (sub_data, new_movie[sub_data]))
                    print("----------------------------------------------------")
                else:
                    print("No result!")
            elif " -tag" not in command and " -index" not in command:
                command_key = str(command).replace("Search:", "")
                target_movies = movie.request_all_movie(command_key)
                if target_movies:
                    index = 0
                    print("Result:")
                    for new_movie in target_movies:
                        key_list = list()
                        print("[%s]:%s" % (index, new_movie["name"]))
                        index += 1
                    print("----------------------------------------------------")
                else:
                    print("No result!")

        elif "update:" in command:
            movie.update()
        elif "count:" in command:
            print("Now I have %s datas." % movie.count)
    except:
        pass
