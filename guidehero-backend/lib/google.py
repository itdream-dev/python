# -*- coding: utf-8 -*-
import requests


def get_google_verification_data(access_token):
    google_auth_url = (
        'https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
    )
    request_url = google_auth_url % access_token

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

    user_request_url = (
        'https://www.googleapis.com/plus/v1/people/%s?access_token=%s'
    )
    request_url = user_request_url % (
        response_dict['user_id'], access_token
    )

    user_response = None
    missed_connections = 0
    while user_response is None:
        try:
            user_response = requests.get(request_url)
        except requests.exceptions.ConnectionError:
            missed_connections += 1
            if missed_connections > 3:
                return {}

    if not user_response.ok:
        return {}

    user_response_dict = user_response.json()

    return {
        'verified': response_dict.get('verified_email'),
        'email': response_dict.get('email'),
        'first_name': user_response_dict.get('name', {}).get('givenName', ''),
        'last_name': user_response_dict.get('name', {}).get('familyName', ''),
        'thumbnail_url': user_response_dict.get('image', {}).get('url', '')
    }
