# -*- coding: utf-8 -*-
import requests


def get_linkedin_data(access_token):
    linkedin_auth_url = (
        'https://api.linkedin.com/v1/people/~:(id,firstName,lastName,'
        'picture-url,headline,public-profile-url,email-address,specialties)'
        '?oauth2_access_token=%s&format=json'
    )
    request_url = linkedin_auth_url % access_token

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

    return {
        "email": response_dict.get('emailAddress'),
        "first_name": response_dict.get('firstName'),
        "last_name": response_dict.get('lastName'),
        "linkedin_profile": response_dict.get('publicProfileUrl'),
        "linkedin_headline": response_dict.get('headline'),
        "thumbnail_url": response_dict.get('pictureUrl')
    }
