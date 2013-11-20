# coding: utf-8
import os
from pprint import pprint
from bitcasa import BitcasaClient


def main():
    client_id = os.environ.get("BITCASA_CLIENT_ID", "")
    client_secret = os.environ.get("BITCASA_CLIENT_SECRET", "")
    access_token = os.environ.get("BITCASA_ACCESS_TOKEN", "")

    assert client_id, 'Please set "BITCASA_CLIENT_ID".'
    assert client_secret, 'Please set "BITCASA_CLIENT_SECRET".'
    assert access_token, 'Please set "BITCASA_ACCESS_TOKEN".'

    bitcasa = BitcasaClient(client_id, client_secret, access_token)
    r = bitcasa.get('folders/', params={'depth': 1})
    pprint(r.json())


if __name__ == '__main__':
    main()
