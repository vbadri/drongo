import json
import http.cookies

from .status_codes import HTTP_STATUS_CODES


class Response(object):
    STATUS_CODE = HTTP_STATUS_CODES[200]
    CONTENT_TYPE = 'text/html'

    def __init__(self, content):
        self.content = content
        self.headers = {}
        self.cookies = http.cookies.BaseCookie()

    def set_header(self, key, value):
        self.headers[key] = value

    def set_cookie(self, key, value):
        self.cookies[key] = value

    def bake(self, start_response):
        body = bytes(self.content, 'utf8')
        self.headers['content-length'] = str(len(body))
        headers = self.headers.items()
        cookies = [('set-cookie', v.OutputString())
                   for _, v in self.cookies.items()]
        if len(self.cookies):
            headers = list(headers) + cookies
        start_response(self.STATUS_CODE, headers)
        return [body]


class JSONResponse(object):
    CONTENT_TYPE = 'application/javascript'

    def __init__(self, obj):
        super(JSONResponse, self).__init__(json.dumps(obj))


class Redirect(object):
    STATUS_CODE = HTTP_STATUS_CODES[303]

    def __init__(self, location):
        self.location = location
        self.headers = {}

    def bake(self, start_response):
        self.headers['location'] = self.location
        headers = self.headers.items()
        start_response(self.STATUS_CODE, headers)
        return []
