import couchdb
import json
from mastodon import Mastodon, StreamListener

# authentication
admin = 'admin'
password = '996996'
url = f'http://{admin}:{password}@127.0.0.1:5984/'

# get the instance
couch_instance = couchdb.Server(url)

# couchdb name
database_name = 'mastodon'

# if the database does not exist, create a new one
if database_name not in couch_instance:
    db = couch_instance.create(database_name)
else:
    db = couch_instance[database_name]

m = Mastodon(
    api_base_url=f'https://aus.social',
    access_token='iROF0h37g3RA78o7DuSv-cgyC3Y1IZ4eFyRyKAeY6cw'
)

class Listener(StreamListener):
    def on_update(self, status):
        json_str = json.dumps(status, indent=2, sort_keys=True, default=str)
        doc_id, doc_rev = db.save(json.loads(json_str))
        print(f'ID: {doc_id} and revision: {doc_rev}')

m.stream_public(Listener())
