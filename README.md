# Census ACS Data to SQLite (or CSV)

### Purpose: to get US Census ACS 5-year data super easily. 

US Census Data (ACS) 5-year data to SQLite database or CSV file.

#### 1. Get your own Census API Key
https://api.census.gov/data/key_signup.html

#### 2. Build a 11-year database (2009-2019) of all the available ACS 5-year variables called census_variables.db using table_shell.py

```python
from table_shells import CreateTableShellDatabase

CreateTableShellDatabase(db_name='sqlite:///data/census_variables.db')
```

#### 3. Get any census data table and write to .csv or to .sqlite database file.  


```python
from census_acs_to_sqlite import CensusTableRequest

census_api_key = '{your_census_api_key}'
# https://api.census.gov/data/key_signup.html

CensusTableRequest(
    census_api_key, 
    year='2019', 
    geography='county', 
    table_id='B19013', 
    out_dir='data/output', 
    file_formats=['sqlite', 'csv'])
```
    
