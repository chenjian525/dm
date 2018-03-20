from tornado.options import options
from tornado.httputil import url_concat
from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    @property
    def db(self):
        """ :rtype: torndb.Connection """
        return self.application.db

    def write_ok(self, **kwargs):
        kwargs['ok'] = True
        self.write(kwargs)

    def write_fail(self, msg=None, **kwargs):
        kwargs.update({
            'ok': False,
            'msg': msg,
        })
        self.write(kwargs)

    def plain_args(self):
        return dict((key, self.get_argument(key)) for key in self.request.arguments)

    def render_string(self, template, **kwargs):
        kwargs['url_concat'] = url_concat
        kwargs['options'] = options
        return super(BaseHandler, self).render_string(template, **kwargs)


class PageNotFound(BaseHandler):
    def get(self):
        self.set_status(404)
        self.render('404.html')

    def post(self):
        self.get()
