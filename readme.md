Ansible module that connects to a postgres database and executes a query against it.

## Example usage:
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
  
- name: display results
  debug: var=result
```

## Result output:
```JSON
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
