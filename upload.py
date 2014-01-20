#!/usr/bin/env python
# coding: utf-8
from __future__ import print_function
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

    path = bitcasa.infinite_drive.path
    print('Upload to InfiniteDrive: ' + path)
    item = bitcasa.upload_file(path, 'upload.py')
    print(item.data)


if __name__ == '__main__':
    main()
