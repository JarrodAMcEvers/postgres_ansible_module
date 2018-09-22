Ansible module that connects to a postgres database and executes a query against it.

Usage in an ansible-playbook:
```
- name: make the query
  postgres_query:
    host: 'localhost'
    port: 5432
    user: 'user'
    password: 'password'
    database: 'database'
    query: 'SELECT * FROM table;'
  register: result
```

Output:
```
{
  "changed": true,
  "results": {
    "rowCount": 1,
    "rows": [
      { "some": "data" }
    ]
  }
}
```
