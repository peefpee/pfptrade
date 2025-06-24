from pymongo import MongoClient


class database:
    def __init__ (self, url: str):
        self.connectionurl = url
        self.client = MongoClient(self.connectionurl)
