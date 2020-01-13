import json
import os
import time
from datetime import datetime, timedelta

from exceptions import FileSizeExceeds, KeyDoesNotExist, KeyExpired
from common import (BASE_OBJECT, FILE_NAME, FILE_PATH, MAX_FILE_SIZE,
                    epoch_time_stamp)


class KVDS(object):
    '''
        KVDS - Key value Data Store
        A file-based key-value data store that
        supports the basic CRD (create, read
        and delete) operations.
    '''

    def __init__(self, filename, filepath=None):
        if filepath is None:
            self.jsonfile = filename
        else:
            self.jsonfile = os.path.join(filepath, filename)

    def create_json_file(self):
        # Create json file for storing key-vaule
        # data with base object 'data'.
        if not os.path.exists(self.jsonfile):
            with open(self.jsonfile, 'w') as f:
                f.write(json.dumps(BASE_OBJECT, indent=2))
                f.close()

    def read_json_file(self):
        # Reads json file key-value data.
        self.create_json_file()
        data = None
        with open(self.jsonfile, 'r') as f:
            data = json.load(f)
            f.close()
        return data

    def update_json_file(self, data):
        # Update data's to json file.
        with open(self.jsonfile, 'w+') as f:
            f.write(json.dumps(data, indent=2))
            f.close()

    def check_file_size(self):
        self.read_json_file()
        # Getting file size in bytes.
        file_size = os.path.getsize(self.jsonfile)
        return file_size

    def check_existing_key(self, key):
        # Checking whether the keyis exist
        # key in the data store.
        data = self.read_json_file()
        return any(key in d for d in data)

    def set_ttl(self, ttl):
        # Setting TTL for the key.
        now = datetime.now()
        ttl = now + timedelta(seconds=ttl)
        # Returnig the epoch time of TTL.
        return epoch_time_stamp(ttl)

    def check_expired(self, ttl):
        # Checking weather the key is expired 
        # or not.
        if ttl > 0:
            now = epoch_time_stamp(datetime.now())
            return ttl < now
        return False

    def create(self, key, value, ttl=None):
        # A new key-value pair is added to
        # the data store.
        file_size = self.check_file_size()
        # checking for file size is lesser
        # than given max file size in bytes.
        if file_size < MAX_FILE_SIZE:
            # Checking for existing key in the
            # data store.
            if not self.check_existing_key(key):
                data = self.read_json_file()
                kv = {}
                kv[key] = str(value)
                if ttl:
                    kv['ttl'] = self.set_ttl(int(ttl))
                else:
                    kv['ttl'] = 0
                data.append(kv)
                self.update_json_file(data)
                print('Successfully created a key "{0}"'.format(key))
            else:
                print('Key "{0}" is already exist!'.format(key))
        else:
            print('File size exceeds {0} bytes'.format(MAX_FILE_SIZE))
            raise FileSizeExceeds

    def read(self, key):
        # A Read operation on a key can
        # be performed by providing the key.
        data = self.read_json_file()
        val = [sub for sub in data if key in sub]
        if val:
            expired = self.check_expired(val[0]['ttl'])
            # Checking for expired.
            if not expired:
                print(val[0][key])
            else:
                print('Key "{0}" is expired!'.format(key))
                raise KeyExpired
        else:
            print('Key "{0}" does not exist!'.format(key))
            raise KeyDoesNotExist

    def delete(self, key):
        # A Delete operation can be
        # performed by providing the key.
        data = self.read_json_file()
        val = [sub for sub in data if key in sub]
        if val:
            expired = self.check_expired(val[0]['ttl'])
            # Checking for expired.
            if not expired:
                data.remove(val[0])
                self.update_json_file(data)
                print('Successfully deleted a key "{0}"'.format(key))
            else:
                print('Key "{0}" is expired!'.format(key))
                raise KeyExpired
        else:
            print('Key "{0}" does not exist!'.format(key))
            raise KeyDoesNotExist


if __name__ == "__main__":
    kvds = KVDS(filename=FILE_NAME, filepath=FILE_PATH)
    # kvds.create('vijay', 'ajith', 300)
    # kvds.read('vijay')
    # kvds.delete('ajith')
