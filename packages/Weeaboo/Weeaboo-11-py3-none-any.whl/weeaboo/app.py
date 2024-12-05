from . import Application
from .util import Pipe
from contextlib import ExitStack
from flask import Flask, g, request
from http import HTTPStatus
from mimetypes import guess_type
from os.path import normpath, pardir
from pathlib import Path
from werkzeug.http import parse_accept_header
import gzip, logging

log = logging.getLogger(__name__)

def _before():
    path = request.full_path
    if path.find('?') == len(path) - 1:
        path = path[:-1]
    log.debug("%s %s for: %s", request.method, path, request.headers.get('User-Agent'))
    g.exitstack = ExitStack().__enter__()

def _teardown(exc):
    try:
        if exc is not None: # Otherwise do it on response close.
            assert not g.exitstack.__exit__(type(exc), exc, exc.__traceback__), 'Cannot suppress exception.'
    except:
        log.exception('Cleanup failed:')

class FlaskApplication(Application):

    def __init__(self, *args, **kwargs):
        self.flask = flask = Flask(*args, **kwargs)
        flask.before_request(_before)
        flask.teardown_request(_teardown)
        class Response(flask.response_class):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.call_on_close(g.exitstack.close)
        flask.response_class = Response

    def __call__(self, environ, start_response):
        return self.flask(environ, start_response)

    def route(self, rule, view_func, **options):
        self.flask.add_url_rule(rule, view_func = view_func, **options)

    def stream(self, basepath, uri): # XXX: Validate hash in query?
        def response(isgz, ungz):
            def close():
                log.debug('Close file.')
                f.close()
            path = gzpath if isgz else ogpath
            t, enc = guess_type(path)
            assert ('gzip' if isgz else None) == enc
            f = gzip.open(path) if ungz else path.open('rb')
            g.exitstack.callback(close)
            r = self.toresponse(HTTPStatus.OK, None, f, mimetype = t)
            if isgz and not ungz:
                r.headers['Content-Encoding'] = enc
            return r # XXX: Add Cache-Control?
        relpath = Path(normpath(uri))
        assert pardir not in relpath.parts
        ogpath = basepath / relpath
        gzpath = ogpath.with_name(f"{ogpath.name}.gz")
        if parse_accept_header(request.headers.get('Accept-Encoding')).quality('gzip'):
            return response(True, False) if gzpath.exists() else response(False, False)
        return response(False, False) if ogpath.exists() else response(True, True)

    def toresponse(self, status, headersornone, payload, **kwargs):
        statusline = f"{status.value} {status.phrase}"
        log.debug("Send: %s", statusline)
        return self.flask.response_class(Pipe(payload) if hasattr(payload, 'read') else payload, statusline, headersornone, **kwargs)
