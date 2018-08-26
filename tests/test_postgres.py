import unittest
from postgres import main, PostgresHandler
from ansible.module_utils import basic
from mock import MagicMock, patch
import psycopg2
from faker import Faker
fake = Faker('it_IT')

class TestPostgresHandler(unittest.TestCase):

    def setUp(self):
        self.postgresHandler = PostgresHandler()

        psycopg2.connect = MagicMock()

        self.module = MagicMock()
        self.module.params = {
            'database': fake.name(),
            'host': fake.name(),
            'port': fake.random_number(4),
            'user': fake.name(),
            'password': fake.name(),
            'query': fake.name()
        }
        self.module.exit_json = MagicMock()
        basic.AnsibleModule = MagicMock(return_value=self.module)

    def testAnsibleModuleIsCreated(self):
        main()

        basic.AnsibleModule.assert_called_with(argument_spec=self.postgresHandler.fields)

    def testConnectsToPostgresDatabaseWithParams(self):
        main()

        psycopg2.connect.assert_called_with(host=self.module.params['host'], database=self.module.params['database'], user=self.module.params['user'], password=self.module.params['password'], port=self.module.params['port'])

    def testExecutesTheQueryGiven(self):
        connection = MagicMock()
        cursor = MagicMock()
        cursor.execute = MagicMock()
        connection.cursor = MagicMock(return_value=cursor)
        psycopg2.connect = MagicMock(return_value=connection)

        main()

        connection.cursor.assert_called()
        cursor.execute.assert_called_with(self.module.params['query'])
