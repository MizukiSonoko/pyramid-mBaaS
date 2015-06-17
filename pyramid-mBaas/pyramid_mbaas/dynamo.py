
import boto.dynamodb
from boto.dynamodb2.table import Table
from boto.dynamodb2.fields import HashKey, RangeKey, KeysOnlyIndex, GlobalAllIndex

class DynamoManager:

    def __init__(self):

        self.Users = Table('Users', schema = [
            HashKey('user_id'),
            RangeKey('name'),
        ], throughput = {
            'read':2,
            'write':2
        }, global_indexes = [
            GlobalAllIndex('EverythingIndex', parts=[
                HahKey('account_type'),
            ], throughput = {
                'read':1,
                'write':1,
            })
        ])

    def init_dynamo(self):
        self.User = Table.create('Users', scheme=[
            HashKey('user_id'),
            RangeKey('name'),
        ], throughput = {
            'read':2,
            'write':2
        }, global_indexes = [
            GlobalAllIndex('EverythingIndex', parts=[
                HahKey('account_type'),
            ], throughput = {
                'read':1,
                'write':1,
            })
        ])

    def update_user(self,user_id, name=None, rank=None, HP=None):
        results = self.User.query(user_id__eq=user_id, index='groupIndex')
        if len(results) != 0:
            return None

        result = results[0]
        print(result['name'], result['rank'])

        if name:
            result['name'] = name
        if rank:
            result['rank'] = rank
        if HP:
            result['HP'] = HP
        result.save(overwrite=True)

        """
        user = self.User.get_item( user_id=user_id, name=name)
        
        user['name'] = name,
        if rank:
            user['rank'] = rank,
        if HP:
            user['HP'] = HP
        user.save(overwrite=True)
        """

    def inser_user(self,user_id=None,name=None,rank=None,HP=None):
        self.User.put_item(data={
            'user_id':user_id,
            'name':   name,
            'rank':   rank,
            'HP'  :   HP
        })

    def exist(user_id):
        try:
            res = DBSession.query(User).filter(User.user_id == user_id).first()
        except(DBAPIError):
            return False
        if res:
            return True

    def get_user(self, name):
        user =  self.Users.get_item(name=name, domain='user')

        user_id = user['user_id']
        name  = user['name']
        rank   = user['rank']
        HP     = user['HP']

if __name__ == "__main__":
    d = DynamoManager()
    d.get('Mizuki')

