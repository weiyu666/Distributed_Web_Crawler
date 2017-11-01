import requests
import re
import json
from multiprocessing import Process
url = "http://bbs.dji.com/"


class Spider:

    class Page:
        _url = ""
        _title = ""

        @staticmethod
        def get_title(content):
            content = str(content)
            start = content.find("<title>") + len("<title>")
            end = content.find("</title>")
            return_str = ""
            for i in range(start, end):
                return_str += content[i]
            return return_str

        @property
        def title(self):
            return self._title

        @property
        def url(self):
            return self._url

        @url.setter
        def url(self, value):
            if isinstance(value, str):
                if value.find("http://") > -1 or value.find("https://") > -1:
                    self._url = value
                    try:
                        content = requests.get(value, timeout=2).text
                    except:
                        content = "<title>ERROR</title>"
                    self._title = self.get_title(content)
                else:
                    raise ValueError("This string isn't an URL!")
            else:
                raise TypeError("The input is not a String type!")

        @staticmethod
        def find_page(page_list, page_url):
            for p in page_list:
                if p.url == page_url:
                    return True
            return False

    _base_url = ""
    s_url = ""

    url_pool = []
    page_pool = []

    @property
    def source_url(self):
        return self.s_url

    @source_url.setter
    def source_url(self, value):

        # is string
        if isinstance(value, str):
            if value.find("http://") > -1 or value.find("https://") > -1:
                self.s_url = value
                # set the base url of this site.
                self._base_url = value.split(
                    "/")[0] + "//" + value.split("/")[2]
            else:
                raise ValueError("This string isn't an URL!")
        else:
            raise TypeError("The input is not a String type!")

    def get_all_url(self, input_url):

        return_url = []
        try:
            content = requests.get(input_url, timeout=5).text
        except requests.ReadTimeout:
            print("TimeOut!")
            return False

        match = re.findall(
            r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')",
            content)

        if len(match) > 0:
            for u in match:
                u.strip('{}()=+_')
                rt_url = ""
                if u.find(r"http://") > -1 or u.find(r"https://") > -1:
                    return_url.append(u)
                else:
                    # Check that is the URL is long enough
                    if len(u) > 2:
                        # eg. /a.php
                        if u[0] == "/" and not u[1] == "/":
                            rt_url = "%s%s" % (r"http:/", u)
                        # eg. //a.php
                        elif u[0] == "/" and u[1] == "/":
                            rt_url = "%s%s" % (r"http:", u)
                        # eg. a.php
                        elif not u[0] == "/":
                            rt_url = self._base_url + "/" + u
                        return_url.append(rt_url)
            return return_url
        else:
            return False

    def grab(self):
        for g_url in self.url_pool:
            print("Finished one term")

            self.url_pool.remove(g_url)
            result = self.get_all_url(g_url)
            if result:
                for u in result:
                    if u not in self.url_pool:

                        if not Spider.Page.find_page(self.page_pool, u):
                            p = Spider.Page()
                            p.url = u
                            self.page_pool.append(p)
                            if not p.title == "ERROR":
                                self.url_pool.append(u)
                                print("%s  %s   %s" %
                                      (p.url, p.title, len(self.url_pool)))

    def asd(self):
        pass

    def grab_new(self):
        for i in range(5):
            try:
                tr = Process(target=self.grab())
                tr.start()
            except:
                pass

    def start(self, times):
        self.url_pool.append(self.source_url)
        time = int(times)
        while time > 0:
            self.grab_new()
            print(
                "Time %d finished!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!" %
                (times - time))

            time -= 1


a = Spider()
a.source_url = url
a.start(2)
