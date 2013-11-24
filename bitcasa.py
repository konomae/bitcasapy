# coding: utf-8
from rauth import OAuth2Session, OAuth2Service


class BitcasaClient(OAuth2Session):
    def __init__(self, client_id, client_secret, access_token=None, service=None, access_token_key=None):
        if not service:
            service = OAuth2Service(
                client_id=client_id,
                client_secret=client_secret,
                name='bitcasa',
                authorize_url='https://developer.api.bitcasa.com/v1/oauth2/authenticate',
                access_token_url='https://developer.api.bitcasa.com/v1/oauth2/access_token',
                base_url='https://developer.api.bitcasa.com/v1/')
        super(BitcasaClient, self).__init__(client_id, client_secret, access_token, service, access_token_key)

    def request(self, method, url, bearer_auth=True, **req_kwargs):
        params = req_kwargs.get('params', {})
        if 'access_token' not in params and self.access_token:
            params['access_token'] = self.access_token
            req_kwargs['params'] = params
        return super(BitcasaClient, self).request(method, url, bearer_auth=bearer_auth, **req_kwargs)
