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

        self.cursor = MagicMock()
        self.cursor.execute = MagicMock()

        self.connection = MagicMock()
        self.connection.cursor = MagicMock(return_value=self.cursor)
        psycopg2.connect = MagicMock(return_value=self.connection)

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
        psycopg2.extras = MagicMock()
        psycopg2.extras.RealDictCursor = MagicMock()

        main()

        self.connection.cursor.assert_called_with(cursor_factory=psycopg2.extras.RealDictCursor)
        self.cursor.execute.assert_called_with(self.module.params['query'])

    def testQueryResultsAreReturnedForTheAnsibleModule(self):
        fetchAllResult = MagicMock()
        self.cursor.fetchall = MagicMock(return_value=fetchAllResult)

        main()

        self.module.exit_json.assert_called_with(changed=False, results=fetchAllResult)

    def testFailAnsibleModuleIfQueryThrowsAnError(self):
        error = psycopg2.ProgrammingError()
        self.cursor.fetchall.side_effect = error

        main()

        self.module.fail_json.assert_called_with(msg="Query failed: {}".format(error))
