# coding: utf-8
from os.path import basename
from rauth import OAuth2Session, OAuth2Service
from requests_toolbelt import MultipartEncoder


class BitcasaException(Exception):
    @classmethod
    def check(cls, data):
        if 'error' in data and data['error']:
            error = data['error']
            raise cls(error.get('message'), error.get('code'))


class BitcasaItem(object):
    def __init__(self, **kwargs):
        self.data = kwargs
        self.name = kwargs.get('name', '')
        self.category = kwargs.get('category', '')
        self.path = kwargs.get('path', '')
        self.type = kwargs.get('type', '')

        self.mirrored = kwargs.get('mirrored', False)
        self.deleted = kwargs.get('deleted', False)
        self.mount_point = kwargs.get('mount_point', '')
        self.status = kwargs.get('status', '')
        self.origin_device_id = kwargs.get('origin_device_id', '')
        self.mtime = kwargs.get('mtime', '')
        self.size = kwargs.get('size', '')
        self.album = kwargs.get('album', '')
        self.id = kwargs.get('id', '')
        self.manifest_name = kwargs.get('manifest_name', '')
        self.extension = kwargs.get('extension', '')
        self.duplicates = kwargs.get('duplicates', [])
        self.incomplete = kwargs.get('incomplete', False)
        self.sync_type = kwargs.get('sync_type', '')

    @property
    def is_folder(self):
        return self.category == 'folders'

    @property
    def is_file(self):
        return not self.is_folder


class BitcasaClient(OAuth2Session):
    def __init__(self, client_id, client_secret, access_token=None, service=None, access_token_key=None):

        self._infinite_drive = None

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

    @property
    def infinite_drive(self):
        """:rtype: BitcasaItem"""

        if not self._infinite_drive:
            # will set infinite drive
            self.do_list_folder('/')
        return self._infinite_drive

    def list_item(self, item=None, category=None):
        """:type item: BitcasaItem"""
        if item:
            if item.is_file:
                raise BitcasaException('Error trying to list a plain file')
            path = item.path
        else:
            bid = self.infinite_drive
            path = bid.path

        return self.do_list_folder(path, category)

    def do_list_folder(self, path='/', category=None):
        device = None
        level = 0
        mf = '/Mirrored Folders'

        if path == '/':
            level = 1
        elif mf == path:
            level = 2
            path = '/'
        elif path.startswith(mf + '/'):
            device = path[len(mf) + 1:]
            level = 3
            path = '/'

        args = {}
        if category:
            args['category'] = category
            args['depth'] = 0
        else:
            # args['depth'] = 1
            pass  # depth = 1 (in php sdk, set but unused (ignore)?)

        r = self.get('folders' + path, params=args)
        if 200 <= r.status_code < 300:
            data = r.json()
            BitcasaException.check(data)
            return self._list_result(data, level, device)
        else:
            raise BitcasaException('Invalid response code', r.status_code)

    def upload_file(self, path, filepath, name=None, exists='rename'):
        name = name if name else basename(filepath)
        endpoint = 'files' + path
        params = {'exists': exists}
        m = MultipartEncoder({'file': (name, open(filepath, 'rb'))})
        r = self.post(endpoint, params=params, headers={'Content-Type': m.content_type}, data=m)
        return self._single_result(r.json())

    def _list_result(self, result, level=0, device=None):
        """:rtype: list[BitcasaItem]"""
        BitcasaException.check(result)
        mirror = False

        items = result['result']['items']
        newres = []
        devices = {}

        for item in items:
            category = item['category']
            name = item['name']
            sync_type = item.get('sync_type')

            if level == 1:  # infinite drive
                if category == 'folders' and sync_type == 'infinite drive':
                    self._infinite_drive = BitcasaItem(**item)

                elif category == 'folders' and (sync_type == 'backup' or sync_type == 'sync' or name == 'Bitcasa Infinite Drive'):
                    if not mirror:
                        mirror = True
                        newres.append(BitcasaItem(**item))
                    continue
                else:
                    newres.append(BitcasaItem(**item))
            elif level == 2:
                if sync_type == 'sync' or sync_type == 'backup':
                    device = item.get('origin_device_id')
                    if devices.get(device):
                        devices[device] = True
                        newres.append(BitcasaItem(device=device))
                continue
            elif level == 3:
                if (sync_type == 'sync' or sync_type == 'backup') and item.get('origin_device_id' == device):
                    newres.append(BitcasaItem(**item))
                continue
            else:
                newres.append(BitcasaItem(**item))
        return newres

    def _single_result(self, data):
        """:rtype: BitcasaItem"""
        BitcasaException.check(data)
        result = self._list_result(data)
        if not result:
            raise BitcasaException('call did not return item information')
        return result[0]

