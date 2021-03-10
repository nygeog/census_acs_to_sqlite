from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///test.db', echo=False)

df = pd.DataFrame({'name' : ['User 1', 'User 2', 'User 3']})

df.to_sql('users', con=engine)

# table name {year}_5yr_acs_{geog}_{table_id}

# generate dictionary by table shells

# keys should be the table id or the stub?

# if sqlite is true,

# # loop through dictionary item(s)
# for table_id in table_id_list:
# 	for year, geography:
#       pull all the data, note if over 50 cols, split.

# 			#	save table_id to .csv

# 			# save table_id to sqlite db.
