import unittest

from pymongo import ReadPreference
from pymongo import MongoClient

import mongoengine
from mongoengine.connection import MongoEngineConnectionError


CONN_CLASS = MongoClient
READ_PREF = ReadPreference.SECONDARY


class ConnectionTest(unittest.TestCase):

    def setUp(self):
        mongoengine.connection._connection_settings = {}
        mongoengine.connection._connections = {}
        mongoengine.connection._dbs = {}

    def tearDown(self):
        mongoengine.connection._connection_settings = {}
        mongoengine.connection._connections = {}
        mongoengine.connection._dbs = {}

    def test_replicaset_uri_passes_read_preference(self):
        """Requires a replica set called "rs" on port 27017
        """

        try:
            conn = mongoengine.connect(db='mongoenginetest',
                           host="mongodb://localhost/mongoenginetest?replicaSet=rs",
                           read_preference=READ_PREF)
        except MongoEngineConnectionError as e:
            return

        if not isinstance(conn, CONN_CLASS):
            # really???
            return

        self.assertEqual(conn.read_preference, READ_PREF)


if __name__ == '__main__':
    unittest.main()
