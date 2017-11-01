import queue
import requests
import json
import re
from bs4 import BeautifulSoup

douban_url_test = "https://movie.douban.com/subject/26711085/?from=subject-page"


class DouBanPage:

    class Score:

        __total_score = ""
        __one_star = ""
        __two_star = ""
        __three_star = ""
        __four_star = ""
        __five_star = ""

        # 总分
        @property
        def total_score(self):
            return self.__total_score

        @total_score.setter
        def total_score(self, value):
            if isinstance(value, float):
                self.__total_score = value
            else:
                raise TypeError("Input not integer!")

        # 一星
        @property
        def one_star(self):
            return self.__one_star

        @one_star.setter
        def one_star(self, value):
            if isinstance(value, float):
                self.__one_star = value
            else:
                raise TypeError("Input not integer!")

        # 二星
        @property
        def two_star(self):
            return self.__two_star

        @two_star.setter
        def two_star(self, value):
            if isinstance(value, float):
                self.__two_star = value
            else:
                raise TypeError("Input not integer!")

        # 三星
        @property
        def three_star(self):
            return self.__three_star

        @three_star.setter
        def three_star(self, value):
            if isinstance(value, float):
                self.__three_star = value
            else:
                raise TypeError("Input not integer!")

        # 四星
        @property
        def four_star(self):
            return self.__four_star

        @four_star.setter
        def four_star(self, value):
            if isinstance(value, float):
                self.__four_star = value
            else:
                raise TypeError("Input not integer!")

        # 五星
        @property
        def five_star(self):
            return self.__five_star

        @five_star.setter
        def five_star(self, value):
            if isinstance(value, float):
                self.__five_star = value
            else:
                raise TypeError("Input not integer!")

    __name = ""
    __year = ""
    __director = ""
    __type = ""
    __region = ""
    __language = ""
    __score = ""
    __tags = list()
    __actors = list()

    # Name
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if isinstance(value, list):
            self.__name = value
        else:
            raise TypeError("Input not list!")

    # year
    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        if isinstance(value, str):
            self.__year = value
        else:
            raise TypeError("Input not string!")

    # director
    @property
    def director(self):
        return self.__director

    @director.setter
    def director(self, value):
        if isinstance(value, str):
            self.__director = value
        else:
            raise TypeError("Input not string!")

    # Type
    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if isinstance(value, list):
            self.__type = value
        else:
            raise TypeError("Input not list!")

    # region
    @property
    def region(self):
        return self.__region

    @region.setter
    def region(self, value):
        if isinstance(value, str):
            self.__region = value
        else:
            raise TypeError("Input not string!")

    # language
    @property
    def language(self):
        return self.__language

    @language.setter
    def language(self, value):
        if isinstance(value, str):
            self.__language = value
        else:
            raise TypeError("Input not string!")

    # tags
    @property
    def tags(self):
        return self.__tags

    @tags.setter
    def tags(self, value):
        if isinstance(value, list):
            self.__tags = value
        else:
            raise TypeError("Input not list!")

    # actors
    @property
    def actors(self):
        return self.__actors

    @actors.setter
    def actors(self, value):
        if isinstance(value, list):
            self.__actors = value
        else:
            raise TypeError("Input not list!")

    # score
    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        if isinstance(value, self.Score):
            self.__score = value
        else:
            raise TypeError("Input not ScoreType!")


class SpiderX:

    __s_url = ""
    __base_url = ""
    url_pool = queue.Queue()
    url_list = list()
    visited_pool = list()
    movie_pool = list()

    @staticmethod
    def is_in_page_pool(page_pool, name):
        for page in page_pool:
            if isinstance(page, DouBanPage):
                if page.name == name:
                    return True
        return False

    @staticmethod
    def is_in_url_pool(url_pool, name):
        for urls in url_pool:
            if isinstance(urls, str):
                if urls == name:
                    return True
        return False

    @property
    def source_url(self):
        return self.__s_url

    @source_url.setter
    def source_url(self, value):
        if isinstance(value, str):
            if "http://" in value or "https://" in value:
                self.__s_url = value
                self.__base_url = value.split(
                    "/")[0] + "//" + value.split("/")[2]
            else:
                raise ValueError("This isn't an URL!")
        else:
            raise TypeError("The input url isn't an String!")

    def analyze_douban(self, input_url):

        def analyze_all_url(input_content):

            match = re.findall(
                r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')",
                input_content)

            if len(match) > 0:
                for u in match:
                    u.strip('{}()=+_')
                    if "movie.douban.com/subject" in u:
                        t = "https://movie.douban.com/subject/"
                        start = u.find("subject/") + len("subject/")
                        end = u.find("/", start)
                        for index in range(start, end):
                            t += u[index]
                        u = t
                        if not SpiderX.is_in_url_pool(self.url_list, u):

                            self.url_pool.put(u)
                            self.url_list.append(u)

                return True
            else:
                return False

        # if the url is a douBan movie page:
        if "movie.douban.com/subject"in input_url and "photos" not in input_url:

            print(input_url)
            self.visited_pool.append(input_url)
            # function to get info of movies.
            try:
                def get_info(page_content):

                    content = page_content
                    objmovie = DouBanPage()
                    soap = BeautifulSoup(content, "html.parser")

                    # get movie name.  cut by bs4 and regex.
                    # (movie_name,as list)

                    movie_name = []

                    # main name
                    movie_name.append(cut_string(
                        str(soap.find(property="v:itemreviewed")), ">", "</"))
                    # alias name
                    alias_regex = re.compile(r"又名:</span>.*<br/>")
                    if not len(alias_regex.findall(content)) == 0:
                        alias_name = cut_string(
                            alias_regex.findall(content)[0],
                            "/span>",
                            "<br/>").strip()
                        movie_name.append(alias_name)
                    print(movie_name)

                    # get movie type.  cut by bs4.
                    # (all_type,as list)
                    type_list = soap.findAll(property="v:genre")
                    all_type = []
                    for t in type_list:
                        all_type.append(
                            cut_string(
                                str(t),
                                "<span property=\"v:genre\">",
                                "</span>"))
                    print(all_type)

                    # get director.   cut by bs4
                    # (director,as string)
                    director = cut_string(str(soap.find(rel="v:directedBy")),
                                          "v:directedBy\">", "</a>")
                    print(director)

                    # get year.   cut by bs4
                    # (year,as string)
                    year = cut_string(str(soap.find(property="v:initialReleaseDate")),
                                      "content=\"", "(")
                    print(year)

                    # get region.   cut by regex.
                    # (region,as string)
                    region_regex = re.compile(r"制片国家/地区.*<br/>")
                    if not len(region_regex.findall(content)) == 0:
                        region = cut_string(
                            region_regex.findall(content)[0],
                            "制片国家/地区:</span>",
                            "<br/>").strip()
                        print(region)
                    else:
                        region = "N/A"

                    # get language.  cut by regex.
                    # (language,as string)
                    language_regex = re.compile(r"语言:.*<br/>")
                    if not len(language_regex.findall(content)) == 0:
                        language = cut_string(
                            language_regex.findall(content)[0],
                            "/span>",
                            "<br/>").strip()
                        print(language)
                    else:
                        language = "N/A"

                    # get TAGs
                    tags = list()
                    all_tags = soap.findAll(attrs={"class": "tags-body"})
                    for line in str(all_tags).split("<"):
                        if "a class" in line:
                            tags.append(
                                cut_string(
                                    line,
                                    "href=\"/tag/",
                                    "\">"))
                    print(tags)

                    # get movie actors.  cut by bs4.
                    # (all_actor,as list)
                    actor_list = soap.findAll(rel="v:starring")
                    all_actor = []
                    for t in actor_list:
                        all_actor.append(
                            cut_string(
                                str(t),
                                "rel=\"v:starring\">",
                                "</a"))
                    print(all_actor)

                    print("-------------------------------------")

                    objmovie.name = movie_name
                    objmovie.type = all_type
                    objmovie.director = director
                    objmovie.year = year
                    objmovie.region = region
                    objmovie.language = language
                    objmovie.actors = all_actor
                    objmovie.tags = tags

                    return objmovie

                # function to get score of movies.
                def get_score(page_content):

                    objscore = DouBanPage.Score()
                    content = page_content

                    try:
                        # get average score:
                        avr = cut_string(
                            content, "property=\"v:average\">", "</strong>")
                        print("Total score=%s" % avr)

                        # get five stars:
                        five_all = cut_string(
                            content, "stars5 starstop", "stars4 starstop")

                        five = float(
                            cut_string(
                                five_all,
                                "rating_per\">",
                                "%</span")) / 100

                        # get four stars:
                        four_all = cut_string(
                            content, "stars4 starstop", "stars3 starstop")
                        four = float(
                            cut_string(
                                four_all,
                                "rating_per\">",
                                "%</span")) / 100

                        # get three stars:
                        three_all = cut_string(
                            content, "stars3 starstop", "stars2 starstop")
                        three = float(
                            cut_string(
                                three_all,
                                "rating_per\">",
                                "%</span")) / 100

                        # get two stars:
                        two_all = cut_string(
                            content, "stars2 starstop", "stars1 starstop")
                        two = float(
                            cut_string(
                                two_all,
                                "rating_per\">",
                                "%</span")) / 100

                        # get one stars:
                        one_all = cut_string(
                            content, "stars1 starstop", " </div>")
                        one = float(
                            cut_string(
                                one_all,
                                "rating_per\">",
                                "%</span")) / 100
                        objscore.five_star = five
                        objscore.four_star = four
                        objscore.three_star = three
                        objscore.two_star = two
                        objscore.one_star = one
                        objscore.total_score = float(avr)

                        return objscore

                    except:
                        print(input_url)
                        return False

                content = requests.get(input_url).text

                s = get_score(content)
                if not s == False:
                    obj_score = s
                    obj_movie = get_info(content)
                    obj_movie.score = obj_score

                    if not SpiderX.is_in_page_pool(
                            self.movie_pool, obj_movie.name):
                        self.movie_pool.append(obj_movie)
                        file = open("result.txt", mode="a", encoding="utf8")
                        info_list = dict()
                        info_list["name"] = obj_movie.name
                        info_list["director"] = obj_movie.director
                        info_list["type"] = obj_movie.type
                        info_list["year"] = obj_movie.year
                        info_list["region"] = obj_movie.region
                        info_list["language"] = obj_movie.language
                        info_list["actors"] = obj_movie.actors
                        info_list["tags"] = obj_movie.tags
                        info_list["total_score"] = obj_movie.score.total_score
                        info_list["five_star"] = obj_movie.score.five_star
                        info_list["four_star"] = obj_movie.score.four_star
                        info_list["three_star"] = obj_movie.score.three_star
                        info_list["two_star"] = obj_movie.score.two_star
                        info_list["one_star"] = obj_movie.score.one_star
                        file.writelines(json.dumps(info_list))
                        file.write("\n")
                        file.close()

                analyze_all_url(content)
            except:
                pass

        # if the url isn't an DouBan url:
        else:
            try:
                content = requests.get(input_url).text
                analyze_all_url(content)
            except requests.exceptions.MissingSchema:
                print(input_url)
            except requests.exceptions.ConnectionError:
                pass

    def analyze_page(self, url, page_type="douBan"):
        if page_type == "douBan":
            self.analyze_douban(url)

    def start(self, max_url_num=1000000):
        if not self.source_url == "":

            self.url_pool.put(self.source_url)
            self.url_list.append(self.source_url)
            count = 0

            while not self.url_pool.empty():

                # if the url is not much than the max num:
                if not count >= max_url_num:
                    new_url = self.url_pool.get(timeout=2)
                    self.url_list.remove(new_url)
                    self.visited_pool.append(new_url)
                    self.analyze_page(new_url)
                else:
                    break

        else:
            raise ValueError("The source_url hasn't been initialized!")


def cut_string(input_str, head, tail):
    if isinstance(
            head,
            str) and isinstance(
            tail,
            str) and isinstance(
                input_str,
            str):
        start = input_str.find(head) + len(head)
        end = input_str.find(tail, start)

        rt_str = ""
        for index in range(start, end):
            rt_str += input_str[index]
        return rt_str
    else:
        raise TypeError("Inputs are not string!")

spider = SpiderX()
spider.source_url = douban_url_test
spider.start()
