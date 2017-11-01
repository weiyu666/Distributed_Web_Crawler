import cherrypy


class Web(object):

    def index(self):
        file = open("record", mode="r")
        read = file.read()
        return read

    index.exposed = True


def start_web_server():
    cherrypy.config.update({'server.socket_host': '192.168.1.251',
                            'server.socket_port': 998,
                            })
    serv = cherrypy.quickstart(Web())
