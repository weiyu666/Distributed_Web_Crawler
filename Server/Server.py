import queue
import socket
import threading
import os
import random


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


class SpiderServer:

    import json

    online = 0
    server = socket.socket()
    url_pool = queue.Queue()
    url_dict = dict()
    visited_pool = dict()
    page_pool = dict()

    # user_agent pool
    ua_pool = list()
    ua_count = 0

    # lists are use for saving the progress
    url_list = list()
    visited_list = list()

    # if new pages come to 1000 or more , try to save.
    page_count = 0

    def load_ua(self):

        file = open("User_Agent_Pool", mode="r", encoding="utf-8")
        line = file.readline()

        while line:
            self.ua_pool.append(line)
            self.ua_count += 1
        file.close()

    def get_ua(self):
        rnd = random.randint(0, self.ua_count - 1)
        return self.ua_pool[rnd]

    def save_url(self):
        pool = open("url_pool", mode="w", encoding="utf-8")
        pool.write(self.json.dumps(self.url_list))
        visited = open("url_visited", mode="w", encoding="utf-8")
        visited.write(self.json.dumps(self.visited_list))
        pool.close()
        visited.close()

    def load_url(self):

        pool = open("url_pool", mode="r", encoding="utf-8")
        content = pool.read()
        pool.close()
        self.url_list = self.json.loads(content)
        for url in self.url_list:
            self.url_pool.put(url)
            self.url_dict[url] = True

        visited = open("url_visited", mode="r", encoding="utf-8")
        content = visited.read()
        visited.close()
        self.visited_list = self.json.loads(content)
        for url in self.visited_list:
            self.visited_pool[url] = True

    def save_page(self):
        file_page = open("page_pool", mode="w", encoding="utf-8")
        for key in self.page_pool:
            page = self.page_pool[key]
            if isinstance(page, DouBanPage):
                file_page.write(page.dump_to_json())
                file_page.write("\n")
        file_page.close()

    def load_page(self):
        file_page = open("page_pool", mode="r", encoding="utf-8")
        line = file_page.readline()
        while line:
            page = DouBanPage()
            page.load_from_json(line)
            self.page_pool[page.name[0]] = page
            line = file_page.readline()

    def save(self):
        self.save_url()
        self.save_page()

    def load(self):
        if os.path.exists("url_pool") and os.path.exists(
                "url_visited") and os.path.exists("page_pool"):
            self.load_page()
            self.load_url()

    def init(self, ip, port):
        # define the server
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((ip, port))
        self.server.listen(50)

    def process(self, sock, addr):

        print(addr)
        self.online += 1

        def is_exist(dict, tag):

            exist = False

            try:
                test = dict[tag]
                exist = True
            except KeyError:
                exist = False

            return exist

        while True:
            data = sock.recv(8192)
            # time.sleep(0.1)
            if not data or data.decode('utf-8') == 'exit':
                self.online -= 1
                file = open("record", mode="w")
                file.write("Online Spider:%s Page Count:%s" %
                           (self.online, len(self.page_pool)))
                file.close()
                break

            content = str(data.decode('utf-8'))
            if "PUT_URL" in content:

                content = content.replace("PUT_URL", "")
                if is_exist(
                        self.visited_pool,
                        content) or is_exist(
                        self.url_dict,
                        content):
                    sock.send(bytes("URL_EXIST", encoding="utf-8"))
                else:
                    # print("Received url:%s" % content)
                    self.url_pool.put(content)
                    self.url_list.append(content)
                    self.url_dict[content] = True
                    sock.send(bytes("FINISHED", encoding="utf-8"))

            if "PUT_PAGE" in content:
                json_content = content.replace("PUT_PAGE", "")
                json_content = str(json_content).replace("b'", "").strip("'")
                obj_movie = DouBanPage()
                if not obj_movie.load_from_json(
                        json_content) == "DECODE_ERROR":
                    # check is the inquiring page exists.
                    is_page_exist = False
                    try:
                        test = self.page_pool[obj_movie.name[0]]
                        is_page_exist = True
                    except KeyError:
                        is_page_exist = False

                    if not is_page_exist:
                        self.page_pool[obj_movie.name[0]] = obj_movie
                        print(
                            "Received page:%s  Count:%s" %
                            (obj_movie.name[0], len(
                                self.page_pool)))

                        self.page_count += 1
                        if self.page_count >= 100:
                            self.page_count = 0

                            self.save()

                        sock.send(bytes("FINISHED", encoding="utf-8"))
                    else:
                        sock.send(bytes("PAGE_EXIST", encoding="utf-8"))
                else:
                    sock.send(bytes("DECODE_ERROR", encoding="utf-8"))

            if "GET_PAGE" in content:
                movie_name = content.replace("GET_PAGE", "")

                # check is the inquiring page exists.
                is_page_exist = False
                try:
                    test = self.page_pool[movie_name]
                    is_page_exist = True
                except KeyError:
                    is_page_exist = False

                if is_page_exist:
                    movie = self.page_pool[movie_name]
                    if isinstance(movie, DouBanPage):
                        sock.send(
                            bytes(
                                movie.dump_to_json(),
                                encoding="utf-8"))
                else:
                    sock.send(bytes("PAGE_NOT_EXIST", encoding="utf-8"))

            if "GET_URL" in content:
                if not self.url_pool.qsize() == 0:
                    new_url = self.url_pool.get()
                    sock.send(bytes(new_url, encoding="utf-8"))
                    if new_url in self.url_list:
                        self.url_list.remove(new_url)
                else:
                    sock.send(bytes("False", encoding="utf-8"))

            if "VISIT_URL" in content:
                url = content.replace("VISIT_URL", "")
                print("Visited url:%s" % url)
                self.visited_pool[url] = True
                self.visited_list.append(url)
                if url in self.url_list:
                    self.url_list.remove(url)

            if "ALL_PAGE" in content:
                sock.send(bytes(str(len(self.page_pool)), encoding="utf-8"))

            if "GET_UA" in content:
                sock.send(bytes(str(self.get_ua()), encoding="utf-8"))

    def start(self):
        self.load()
        # loop
        while True:

            self.load_ua()

            sock, addr = self.server.accept()
            file = open("record", mode="w")
            file.write("Online Spider:%s Page Count:%s" %
                       (self.online, len(self.page_pool)))
            file.close()
            t = threading.Thread(target=self.process, args=(sock, addr))
            t.start()


# start_web_server()
server = SpiderServer()
server.init(open("ip", mode="r").read(), 8099)

server.start()
