import socket
import threading
import queue


class DouBanPage:

    import json

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
            if isinstance(value, str):
                self.__total_score = value
            else:
                raise TypeError("Input not integer!")

        # 一星
        @property
        def one_star(self):
            return self.__one_star

        @one_star.setter
        def one_star(self, value):
            if isinstance(value, str):
                self.__one_star = value
            else:
                raise TypeError("Input not integer!")

        # 二星
        @property
        def two_star(self):
            return self.__two_star

        @two_star.setter
        def two_star(self, value):
            if isinstance(value, str):
                self.__two_star = value
            else:
                raise TypeError("Input not integer!")

        # 三星
        @property
        def three_star(self):
            return self.__three_star

        @three_star.setter
        def three_star(self, value):
            if isinstance(value, str):
                self.__three_star = value
            else:
                raise TypeError("Input not integer!")

        # 四星
        @property
        def four_star(self):
            return self.__four_star

        @four_star.setter
        def four_star(self, value):
            if isinstance(value, str):
                self.__four_star = value
            else:
                raise TypeError("Input not integer!")

        # 五星
        @property
        def five_star(self):
            return self.__five_star

        @five_star.setter
        def five_star(self, value):
            if isinstance(value, str):
                self.__five_star = value
            else:
                raise TypeError("Input not integer!")

    __url = ""
    __name = ""
    __year = ""
    __director = ""
    __type = ""
    __region = ""
    __language = ""
    __score = ""
    __tags = list()
    __actors = list()

    # URL
    @property
    def url(self):
        return self.__url

    @url.setter
    def url(self, value):
        if isinstance(value, str):
            self.__url = value
        else:
            raise TypeError("Input not str!")

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

    def dump_to_json(self):
        info_list = dict()
        info_list["url"] = self.url
        info_list["name"] = self.name
        info_list["director"] = self.director
        info_list["type"] = self.type
        info_list["year"] = self.year
        info_list["region"] = self.region
        info_list["language"] = self.language
        info_list["actors"] = self.actors
        info_list["tags"] = self.tags
        info_list["total_score"] = "%.2f" % float(self.score.total_score)
        info_list["five_star"] = "%.2f" % float(self.score.five_star)
        info_list["four_star"] = "%.2f" % float(self.score.four_star)
        info_list["three_star"] = "%.2f" % float(self.score.three_star)
        info_list["two_star"] = "%.2f" % float(self.score.two_star)
        info_list["one_star"] = "%.2f" % float(self.score.one_star)
        return self.json.dumps(info_list)

    def load_from_json(self, json):
        try:
            info_list = self.json.loads(json)
            self.url = info_list["url"]
            self.name = info_list["name"]
            self.director = info_list["director"]
            self.type = info_list["type"]
            self.year = info_list["year"]
            self.region = info_list["region"]
            self.language = info_list["language"]
            self.actors = info_list["actors"]
            self.tags = info_list["tags"]
            self.score = DouBanPage.Score()
            self.score.total_score = info_list["total_score"]
            self.score.five_star = info_list["five_star"]
            self.score.four_star = info_list["four_star"]
            self.score.three_star = info_list["three_star"]
            self.score.two_star = info_list["two_star"]
            self.score.one_star = info_list["one_star"]
        except self.json.decoder.JSONDecodeError:
            return "DECODE_ERROR"


class Client:

    __sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __is_connected = False

    def connect(self, ip, port):
        self.__sock.connect((ip, port))
        self.__is_connected = True

    def disconnect(self):
        self.__sock.close()

    def put_url(self, url):

        self.__sock.send(
            bytes(
                "PUT_URL%s" %
                url,
                encoding="utf-8"))
        result = str(self.__sock.recv(1024).decode("utf-8"))
        if result == "FINISHED":
            return True
        elif result == "URL_EXIST":
            return False
        else:
            return False

    def put_page(self, page):
        json_text = page.dump_to_json()
        self.__sock.send(
            bytes(
                "PUT_PAGE%s" %
                json_text,
                encoding="utf-8"))

        result = str(self.__sock.recv(1024).decode("utf-8"))
        print(str(result))
        if result == "FINISHED":
            return True
        elif result == "PAGE_EXIST":
            return False
        else:
            return False

    def get_url(self):
        self.__sock.send(
            bytes("GET_URL", encoding="utf-8"))
        result = str(self.__sock.recv(1024).decode("utf-8"))
        return result

    def visit_url(self, url):
        self.__sock.send(
            bytes("VISIT_URL%s" % url, encoding="utf-8"))

    def get_page(self, page_name):
        self.__sock.send(
            bytes(
                "GET_PAGE%s" %
                page_name,
                encoding="utf-8"))
        result = str(self.__sock.recv(1024).decode("utf-8"))
        if not result == "PAGE_NOT_EXIST":
            p = DouBanPage()
            p.load_from_json(str(result))
            return p
        else:
            return False
