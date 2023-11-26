import email
import pprint
from io import StringIO

class ReqParser:
    def __init__(self, raw_req):
        res = raw_req.split('\r\n', 1)
        req_target, headers = raw_req.split('\r\n', 1)
        self._method, self._url, self._version = req_target.split()
        message = email.message_from_string(headers)
        self._headers = dict(message.items())

    def __repr__(self):
        s = StringIO()
        print(self._method, self._url, self._version, file=s)
        pprint.pprint(self._headers, stream=s, width=160)
        return s.getvalue()

    @property
    def method(self):
        return self._method
    
    @property
    def url(self):
        return self._url

    @property
    def version(self):
        return self._version

    @property
    def headers(self):
        return self._headers
    
    def get_cookies(self):
        cookies = self._headers.get('Cookie', None)
        if cookies is None:
            return {}
        
        return dict(i.strip().split('=') for i in cookies.split(';'))

if __name__ == '__main__':
    text = "GET / HTTP/1.1\r\nHost: localhost\r\nConnection: keep-alive\r\nCache-Control: max-age=0\r\nUpgrade-Insecure-Requests: 1\r\nUser-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8\r\nAccept-Encoding: gzip, deflate, sdch\r\nAccept-Language: en-US,en;q=0.8'"
    rp = ReqParser(text)

    print(rp)