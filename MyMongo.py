import pymongo


class myDB:
    def __init__(self, db_name):
        self.myclient = pymongo.MongoClient('mongodb://localhost:27017/')
        self.mydb = self.myclient[db_name]

    def select_table(self, table_name):
        self.mycol = self.mydb[table_name]

    def insert(self, data):
        self.select_table(data.pop('dbid'))
        self.mycol.insert_one(data)
