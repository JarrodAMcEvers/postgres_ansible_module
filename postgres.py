#!/usr/bin/python
from ansible.module_utils import basic
from ansible.module_utils.basic import *

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

def main():
    postgresHandler = PostgresHandler()
    module = basic.AnsibleModule(argument_spec=postgresHandler.fields)
    module.exit_json(changed=False, meta={ "hello": "world" })

if __name__ == '__main__':
    main()
