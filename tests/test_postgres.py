import unittest
from postgres import main, PostgresHandler
from ansible.module_utils import basic
from mock import MagicMock

class test_postgres_query(unittest.TestCase):

    def setUp(self):
        self.postgresHandler = PostgresHandler()

    def testAnsibleModuleIsCreated(self):
        module = MagicMock()
        module.exit_json = MagicMock()
        basic.AnsibleModule = MagicMock(return_value=module)

        main()

        basic.AnsibleModule.assert_called_with(argument_spec=self.postgresHandler.fields)
