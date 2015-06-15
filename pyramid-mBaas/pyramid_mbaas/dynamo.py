
import boto.dynamodb
from boto.dynamodb2.table import Table

class DynamoManager:

    def __init__(self):
        self.Users = Table('Users')

    def get(self, name):
        user =  self.Users.get_item(name=name, domain='user')

        account  = user['name']
        rank   = user['rank']
        HP     = user['HP']
        print( account)

if __name__ == "__main__":
    d = DynamoManager()
    d.get('Mizuki')

