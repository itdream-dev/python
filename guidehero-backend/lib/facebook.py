# -*- coding: utf-8 -*-
import hmac
import hashlib
import requests
from config import Ivysaur


def get_facebook_verification_data(access_token):
    """
    Given an access token, ask Facebook for its id
    Implicitly, this also checks that the access token is valid
    """
    h = hmac.new(Ivysaur.Config.FACEBOOK_KEY.encode('utf-8'),
                 msg=access_token.encode('utf-8'),
                 digestmod=hashlib.sha256)
    appsecret_proof = h.hexdigest()
    graph_url = "https://graph.facebook.com/me"

    additional_fields = ['verified', 'email', 'first_name', 'last_name', 'id']

    params = {
        'access_token': access_token,
        'appsecret_proof': appsecret_proof,
        'fields': ','.join(additional_fields)
    }
    request_url = graph_url + '?' + '&'.join("%s=%s" % (k, v)
                                             for k, v in params.items())

    response = None
    missed_connections = 0
    while response is None:
        try:
            response = requests.get(request_url)
        except requests.exceptions.ConnectionError:
            missed_connections += 1
            if missed_connections > 3:
                return {}

    if not response.ok:
        return {}

    response_dict = response.json()

    picture_url = 'https://graph.facebook.com/v2.7/%s/picture' % (
        response_dict.get('id', '')
    )
    params = {
        'access_token': access_token,
        'appsecret_proof': appsecret_proof,
        'type': 'normal',
        'redirect': 0
    }
    request_url = picture_url + '?' + '&'.join("%s=%s" % (k, v)
                                             for k, v in params.items())
    picture_response = None
    missed_connections = 0
    while picture_response is None:
        try:
            picture_response = requests.get(request_url)
        except requests.exceptions.ConnectionError:
            missed_connections += 1
            if missed_connections > 3:
                return {}

    if not response.ok:
        return {}

    picture_response_dict = picture_response.json()

    return {
        'verified': response_dict.get('verified'),
        'email': response_dict.get('email'),
        'first_name': response_dict.get('first_name', ''),
        'last_name': response_dict.get('last_name', ''),
        'thumbnail_url': picture_response_dict.get('data', {}).get('url', '')
    }