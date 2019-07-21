from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


class Mongod(object):

    def __init__(self, username="xidongc", pwd="chen19910531", local=False):
        self.client = None
        url = "mongodb+srv://"+username + ":" + pwd + "@cluster0-xhald.mongodb.net/test?retryWrites=true&w=majority"
        self._connect(url)
        self.db = self.client.blog

    def _connect(self, url):
        self.client = MongoClient(url)
        try:
            status = self.client.admin.command("serverStatus")
            # print("### Server Status ###")
            # pprint.pprint(status)

        except ConnectionFailure:
            print("Connection can not be established")
