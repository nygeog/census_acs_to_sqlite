# Census ACS Data to SQLite (or CSV)

### Purpose: to Census data super easily. 

US Census Data (ACS) 5-year data to SQLite database

## 1. Build a 11-year database called `data/census_variables.db` using `tools/table_shell.py`

```python
from table_shells import CreateTableShellDatabase

CreateTableShellDatabase('sqlite:///../data/census_variables.db')
```

##  2. Get any census data table and write to `.csv` or to `.sqlite` database file.  


```python
from census_acs_to_sqlite import CensusTableRequest

census_api_key = '{your_census_api_key}'
# https://api.census.gov/data/key_signup.html

CensusTableRequest(
    census_api_key, '2019', 'county', 'B19013', 
    'data/output', ['csv', 'sqlite'])
```
    
