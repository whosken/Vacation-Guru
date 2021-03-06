import pymongo

import os

HOST = os.environ.get('MONGODB_URI') or 'mongodb://localhost:27017/destinate'

class LazyClient(object):
    def __init__(self):
        self._client = False
        
    def __getattr__(self,name):
        if name == '_client':
            return self._client
        if not self._client:
            print 'connecting to', HOST
            db_name = pymongo.uri_parser.parse_uri(HOST).get('database')
            self._client = pymongo.MongoClient(HOST)[db_name]
        return getattr(self._client, name)
    
db = LazyClient()
