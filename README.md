# Bitcasa API Python Client (Unofficial)


## Requirements

- Tested with Python 2.7.6 and Python 3.3.2 on Mac OS X 10.9
- Bitcasa API v1
- requests v1.x
- rauth

See `requirements.txt`

```bash
$ pip install -r requirements.txt
```


## Get Access Token

First, register your app in [Bitcasa API Console](https://developer.bitcasa.com/admin/applications)

```bash
$ export BITCASA_CLIENT_ID="<your_client_id>"
$ export BITCASA_CLIENT_SECRET="<your_client_secret>"
$ python get_access_token.py
Please go to https://developer.api.bitcasa.com/v1/oauth2/authenticate?client_id=<client_id> and authorize access.
Enter the full callback URL: https://developer.api.bitcasa.com/v1/oauth2/accessing?authorization_code=<authorization_code>#/authenticate?client_id=<client_id>
access_token: <access_token>
```


## Usage

### Example Python Code

```python
from bitcasa import BitcasaClient

client_id = '<your_client_id>'
client_secret = '<your_client_secret>'
access_token = '<your_access_token>'

bitcasa = BitcasaClient(client_id, client_secret, access_token)
items = bitcasa.list_item()
for i in items:
    print(i.name)
```

### Run example

```bash
$ export BITCASA_CLIENT_ID="<your_client_id>"
$ export BITCASA_CLIENT_SECRET="<your_client_secret>"
$ export BITCASA_ACCESS_TOKEN="<your_access_token>"
$ python example.py
(list bitcasa folders)

$ python upload.py
(upload upload.py to infinite drive)
```

BitcasaClient built on rauth's OAuth2Session. OAuth2Session built on requests's Session.

So, You can use same API of requests.
