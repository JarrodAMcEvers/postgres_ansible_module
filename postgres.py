#!/usr/bin/python
from ansible.module_utils import basic
from ansible.module_utils.basic import *
import psycopg2 as psql
import psycopg2.extras
import json

class PostgresHandler():
    def __init__(self):
        self.fields = self.getArgumentsSpec()

    def getArgumentsSpec(self):
        return {
            "host": { "required": True, "type": "str" },
            "port": { "required": True, "type": "int" },
            "user": { "required": True, "type": "str" },
            "password": { "required": True, "type": "str" },
            "database": { "required": True, "type": "str" },
            "query": { "required": True, "type": "str" },
        }

    def setModuleParams(self, module_params):
        self.host = module_params['host']
        self.port = module_params['port']
        self.user = module_params['user']
        self.password = module_params['password']
        self.database = module_params['database']
        self.query = module_params['query']

    def executeQuery(self):
        self.cursor.execute(self.query)
        return self.cursor.fetchall()

    def connectToDatabase(self):
        self.connection = psql.connect(host=self.host, port=self.port, user=self.user, password=self.password, database=self.database)
        self.cursor = self.connection.cursor(cursor_factory=psql.extras.RealDictCursor)


def main():
    postgresHandler = PostgresHandler()
    module = basic.AnsibleModule(argument_spec=postgresHandler.fields)
    postgresHandler.setModuleParams(module.params)
    postgresHandler.connectToDatabase()
    result = postgresHandler.executeQuery()
    module.exit_json(changed=False, result=result)

if __name__ == '__main__':
    main()
