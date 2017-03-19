import cgi
import http.cookies

from .utils import dict2


class Request(object):

    __slots__ = ['env', '_query', '_cookies', '_context']

    def __init__(self, env):
        self.env = env
        self._context = dict2()

        # Load the query params and form params
        env.setdefault('QUERY_STRING', '')
        inp = env.get('wsgi.input')
        self._query = dict2()
        fs = cgi.FieldStorage(inp, environ=env)
        for k in fs:
            fld = fs[k]
            is_file = False
            try:
                it = iter(fld)
                for item in it:
                    if hasattr(item, 'filename') and item.filename:
                        is_file = True
            except TypeError:
                if hasattr(fld, 'filename') and fld.filename:
                    is_file = True
            if not is_file:
                fld = fs.getlist(k)
            self._query[k] = fld

        # Load the cookies
        self._cookies = dict2()
        for cookie in http.cookies.BaseCookie(env.get('HTTP_COOKIE')).values():
            self._cookies[cookie.key] = cookie.value

    @property
    def method(self):
        return self.env['REQUEST_METHOD'].upper()

    @property
    def path(self):
        return self.env['PATH_INFO']

    @property
    def query(self):
        return self._query

    @property
    def cookies(self):
        return self._cookies

    @property
    def context(self):
        return self._context
