import logging
from werkzeug.wrappers import Request


logger = logging.getLogger('')


class RequestLoggerMiddleware(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if environ['PATH_INFO'] == '/log.txt':
            return self.app(environ, start_response)
        header = {}

        def callback(status, headers, exc_info=None):
            header.update({
                'status': status,
                'headers': headers
            })
            start_response(status, headers, exc_info)

        environ = self.log_request(environ)
        response = self.app(environ, callback)
        chunks = [chunk for chunk in response]
        body = ''.join(chunks)
        logger.info('HEAD:\n{}'.format(header))
        is_ajax = False
        for key, value in header['headers']:
            if key == 'Content-Type':
                if value == 'application/json':
                    is_ajax = True
        if is_ajax:
            logger.info('BODY:\n{}\n'.format(body))
        return chunks

    def log_request(self, environ):
        from io import BytesIO
        length = environ.get('CONTENT_LENGTH', '0')
        length = 0 if length == '' else int(length)

        body = environ['wsgi.input'].read(length)
        environ['wsgi.input'] = BytesIO(body)

        request = Request(environ)
        method = str(request.method)
        data = {
            'body': str(request.data),
            'method': method
        }
        logger.info('Request\n{}'.format(data))

        environ['wsgi.input'] = BytesIO(body)
        return environ
