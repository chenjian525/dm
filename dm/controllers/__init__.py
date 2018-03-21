import logging
import voluptuous
from tornado.options import options
from tornado.httputil import url_concat, responses
from tornado.web import RequestHandler, HTTPError
from tornado import escape


class APIError(Exception):
    pass


def get_error_message(ex):
    if isinstance(ex, (list, tuple)):
        ex = ex[0]
        return get_error_message(ex)

    if isinstance(ex, Exception):
        ex = ex.args[0]
        return get_error_message(ex)

    if isinstance(ex, str):
        return ex


class BaseHandler(RequestHandler):

    @property
    def db(self):
        """ :rtype: torndb.Connection """
        return self.application.db

    def write_ok(self, chunk):
        res = {
            'ok': True,
            'body': chunk
        }

        self.write(res)

    def write_error(self, status_code, **kwargs):
        result = {
            'ok': False,
            'error': {
                'message': 'Internal Server Error',
            }
        }

        if 'exc_info' in kwargs:
            try:
                exception = kwargs['exc_info'][1]

                if isinstance(exception, HTTPError):
                    # 一般的 HTTPError
                    message = (exception.reason or
                               exception.log_message or
                               responses.get(exception.status_code,
                                             'Unknown'))

                    result['error']['message'] = message

                elif isinstance(exception, voluptuous.error.Error):
                    # 参数校验错误
                    errors = []
                    if isinstance(exception, voluptuous.error.MultipleInvalid):
                        errors = exception.errors
                    elif isinstance(exception, voluptuous.error.Invalid):
                        errors = [exception]
                    elif isinstance(exception, voluptuous.error.MatchInvalid):
                        errors = [exception]

                    self.set_status(400)
                    result['error']['message'] = get_error_message(exception)
                    invalid_params = ['.'.join(map(str, e.path))
                                      for e in errors if e.path]
                    if invalid_params:
                        result['error']['params'] = invalid_params

                elif isinstance(exception, APIError):
                    result['error']['message'] = ' '.join(exception.args)

            except Exception as e:
                logging.exception(e)

        self.set_header("Content-Type", "application/json; charset=UTF-8")
        chunk = escape.json_encode(result)
        self.finish(chunk)

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
