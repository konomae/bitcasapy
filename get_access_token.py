#!/usr/bin/env python
# coding: utf-8
import os
try:
    import urlparse
except ImportError:
    from urllib import parse as urlparse
from rauth import OAuth2Service


def main():
    client_id = os.environ.get("BITCASA_CLIENT_ID", "")
    client_secret = os.environ.get("BITCASA_CLIENT_SECRET", "")

    assert client_id, 'Please set "BITCASA_CLIENT_ID".'
    assert client_secret, 'Please set "BITCASA_CLIENT_SECRET".'

    oauth = OAuth2Service(
        client_id=client_id,
        client_secret=client_secret,
        name='bitcasa',
        authorize_url='https://developer.api.bitcasa.com/v1/oauth2/authenticate',
        access_token_url='https://developer.api.bitcasa.com/v1/oauth2/access_token',
        base_url='https://developer.api.bitcasa.com/v1')
    authorization_url = oauth.get_authorize_url()
    print('Please go to %s and authorize access.' % authorization_url)

    try:
        authorization_response = raw_input('Enter the full callback URL: ')
    except:
        authorization_response = input('Enter the full callback URL: ')

    query = urlparse.urlparse(authorization_response).query
    params = dict(urlparse.parse_qsl(query))

    authorization_code = params['authorization_code']
    r = oauth.get_raw_access_token('GET', params={'code': authorization_code, 'secret': client_secret})
    data = r.json()
    access_token = data['result']['access_token']
    print('access_token:', access_token)


if __name__ == '__main__':
    main()
