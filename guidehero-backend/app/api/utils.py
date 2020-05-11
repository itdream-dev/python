from functools import wraps
from flask import jsonify, Response
from flask import current_app
import logging
from flask import request
from werkzeug.exceptions import BadRequest
import pprint
import io
import traceback


logger = logging.getLogger('api')
logger = logging.getLogger('')


def dict_to_response(f):
    @wraps(f)
    def inner(*args, **kwargs):
        try:
            logger.debug('Request to {}\nargs={}\nparams={}'.format(
                f, request.args, _get_params(request))
            )
            r = f(*args, **kwargs)
            logger.debug(
                'Handler response:\n{}'.format(show_handler_result(r))
            )
        except Exception as ex:
            if current_app.config.get('DEBUG'):
                try:
                    save_error_to_file(ex, request)
                except Exception as ex:
                    print(
                        'Unhandled exception while saving error report: {}'
                    ).format(str(ex))
            logger.error('Error: "{}". params: "{}", args="{}"'.format(
                str(ex), _get_params(request), request.args
            ))
            if current_app.config.get('DEBUG'):
                print(str(ex))
                return jsonify({'error': str(ex)}), 400
            code = 400
            if not isinstance(ex, ValueError):
                code = 500
            return jsonify({'error': str(ex)}), 400
        response, code = convert_to_response(r)
        return response, code
    return inner


def save_error_to_file(ex, request):
    with open('error_report.txt', 'w') as f:
        f.write('Error: "{}". params: "{}", args="{}"'.format(
            str(ex), _get_params(request), request.args
        ))
        f.write('\n------------------\n')
        traceback.print_exc(file=f)


def show_handler_result(r):
    if not current_app.config.get('DEBUG'):
        return 'AVAILALBE ONLY FOR DEBUG LEVEL OF LOGGING'
    if isinstance(r, Response):
        return r.get_data()

    if isinstance(r, tuple) and isinstance(r[0], Response):
        return r[0].get_data()

    st = io.BytesIO()
    pprint.pprint(r, stream=st)
    return st.getvalue()


def convert_to_response(r):
    if isinstance(r, dict):
        return jsonify(r), '200 OK'
    if isinstance(r, Response):
        return r, None
    if isinstance(r, tuple):
        code = r[1]
        data = r[0]
        if isinstance(data, Response):
            return data, code
        else:
            return jsonify(data), code
    ex = (
        'Response type {} is not support by decorator @dict_to_response'
    ).format(type(r))
    raise Exception(ex)


def _get_params(request):
    try:
        return request.json
    except BadRequest:
        return None
