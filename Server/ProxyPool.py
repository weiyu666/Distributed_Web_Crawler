import queue
import requests
import socket

headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; Maxthon/3.0)'
}

print(requests.get("http://www.cybersyndrome.net/search.cgi?q=&a=&f=&s=&n=",headers=headers).text)