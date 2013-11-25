#!/usr/bin/env python
# coding: utf-8
import os
from bitcasa import BitcasaClient


def main():
    client_id = os.environ.get("BITCASA_CLIENT_ID", "")
    client_secret = os.environ.get("BITCASA_CLIENT_SECRET", "")
    access_token = os.environ.get("BITCASA_ACCESS_TOKEN", "")

    assert client_id, 'Please set "BITCASA_CLIENT_ID".'
    assert client_secret, 'Please set "BITCASA_CLIENT_SECRET".'
    assert access_token, 'Please set "BITCASA_ACCESS_TOKEN".'

    bitcasa = BitcasaClient(client_id, client_secret, access_token)

    r = bitcasa.get('folders/')
    data = r.json()

    infinite_drive = {}
    for folder in data['result']['items']:
        if folder.get('sync_type') == 'infinite drive':
            infinite_drive = folder
            break
    assert infinite_drive

    path = 'files' + infinite_drive['path']
    print('Upload to InfiniteDrive: ' + path)

    with open('upload.py', 'rb') as f:
        r = bitcasa.post(path, files={'file': f})
        print(r.text)


if __name__ == '__main__':
    main()
