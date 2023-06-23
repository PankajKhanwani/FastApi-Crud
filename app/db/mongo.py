import motor.motor_asyncio
from datetime import datetime
import uuid
import logging

logging.getLogger().setLevel(logging.DEBUG)
LOG = logging.getLogger(__name__)


class Mongo:
    """
    Mongo database class
    """

    def __init__(self):
        self.conn = 'mongodb://localhost:27017'
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.conn)
        self.db = self.client['test_app']

    async def add(self, collection: str, document: dict):
        """
        Add a document
        """
        try:
            document = dict(document)
            document.pop('repeat_password')
            if 'uuid' not in document:
                uid = str(uuid.uuid4())
                document['uuid'] = uid
            else:
                uid = document['uuid']
            document['created_at'] = datetime.now()
            await self.db[collection].insert_one(document)
            return uid
        except Exception as e:
            LOG.error(f"Exception occurred at db: {str(e)}")
            raise e

    async def delete(self, collection: str, document: dict):
        """
        Delete a document
        """
        try:
            print(document)
            return self.db[collection].delete_one(document)
        except Exception as e:
            LOG.error(f"Exception occurred at db: {str(e)}")
            raise e

    async def update(self, collection: str, uid: str, document: dict, upsert: bool = False):
        """
        Update a document
        """
        try:
            document.update({'updated_at': datetime.now()})
            return self.db[collection].update_one({'uuid': uid}, {'$set': document}, upsert=upsert)
        except Exception as e:
            LOG.error(f"Exception occurred at db: {str(e)}")
            raise e

    async def find(self, collection: str, filter_dict: dict = None, projection_dict: dict = {}):
        """
        Find a document
        """
        try:
            projection_dict.update({'_id': 0})
            documents = self.db[collection].find(filter_dict, projection_dict)
            docs = await documents.to_list(length=1000)
            return docs
        except Exception as e:
            LOG.error(f"Exception occurred at db: {str(e)}")
