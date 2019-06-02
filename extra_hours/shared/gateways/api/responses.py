from flask import jsonify


def ok(data):
    response = _make_response(data=data)
    return response, 200


def created(data):
    response = _make_response(data=data)
    return response, 201


def bad_request(errors):
    response = _make_response(errors=errors)
    return response, 400


def no_authorized(errors):
    response = _make_response(errors=errors)
    return response, 401


def _make_response(data=None, errors=()):
    return jsonify({'data': data, 'errors': errors})
