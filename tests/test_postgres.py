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

    def testAnsibleModuleIsCreated(self):
        module = MagicMock()
        module.exit_json = MagicMock()
        basic.AnsibleModule = MagicMock(return_value=module)

        main()

        basic.AnsibleModule.assert_called_with(argument_spec=self.postgresHandler.fields)

    def testConnectsToPostgresDatabaseWithParams(self):
        module = MagicMock()
        module.params = {
            'database': fake.name(),
            'host': fake.name(),
            'port': fake.random_number(4),
            'user': fake.name(),
            'password': fake.name(),
            'query': fake.name()
        }
        module.exit_json = MagicMock()
        basic.AnsibleModule = MagicMock(return_value=module)
        psycopg2.connect = MagicMock()

        main()

        psycopg2.connect.assert_called_with(host=module.params['host'], database=module.params['database'], user=module.params['user'], password=module.params['password'], port=module.params['port'])

    def testExecutesTheQueryGiven(self):
        module = MagicMock()
        module.params = {
            'database': fake.name(),
            'host': fake.name(),
            'port': fake.random_number(4),
            'user': fake.name(),
            'password': fake.name(),
            'query': fake.name()
        }
        module.exit_json = MagicMock()
        basic.AnsibleModule = MagicMock(return_value=module)
        connection = MagicMock()
        cursor = MagicMock()
        cursor.execute = MagicMock()
        connection.cursor = MagicMock(return_value=cursor)
        psycopg2.connect = MagicMock(return_value=connection)

        main()

        connection.cursor.assert_called()
        cursor.execute.assert_called_with(module.params['query'])
