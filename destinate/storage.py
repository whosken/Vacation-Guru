import elastic
import mongo
import datetimeutc

from elastic import PAGING_OPTIONS

def upsert_user(user):
    query = {'_id':hash(user['facebook_id'])}
    update = {
        '$set':user,
        '$currentDate':{'last_login':True},
        }
    mongo.db.users.update_one(query, update, upsert=True)
    return True
    
def get_user_by_id(facebook_id, valid_days=30, fields=None):
    then = datetimeutc.Datetime.now() - datetime.timedelta(days=valid_days)
    query = {'_id':hash(facebook_id), 'last_login':{'$gte':then}}
    return mongo.db.users.find_one(query, fields)
    
def get_user_by_token(token, valid_minutes=360, fields=None):
    ''' Invalidate token if it's older than valid_minutes '''
    then = datetimeutc.Datetime.now() - datetime.timedelta(minutes=valid_minutes)
    query = {'token':token, 'last_login':{'$gte':then}}
    return mongo.db.users.find_one(query, fields)

def upsert_cities(cities, reset=False):
    if reset:
        elastic.delete_index()
    elastic.create_index()
    actions = map(create_city_upsert, cities)
    elastic.helpers.bulk(
        elastic.client,
        actions,
        request_timeout=60)
    elastic.refresh_index()
    return True
    
def search_cities(query=None, **options):
    if 'fields' not in options:
        options['fields'] = [
            'name',
            'cid',
            'regions',
            'location',
            'images'
            ]
    return elastic.search(
        query,
        index=elastic.SEARCH_INDEX,
        **options)

def create_city_upsert(city):
    return {
        '_op_type':'update',
        '_id':hash(city['cid']),
        '_index':elastic.SEARCH_INDEX,
        '_type':'city',
        'doc':city,
        'doc_as_upsert': True
        }
