from sqlalchemy import create_engine
import pandas as pd
from tools.census_api import CensusACS5Year
import sqlite3
from tools.helpers import read_json


pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class CensusTableRequest:
    def __init__(
            self, api_key, year, geography, table_id, out_dir, file_format=None
    ):
        self.api_key = api_key
        self.year = year
        self.geography = geography
        self.table_id = table_id
        if file_format is None:
            file_format = ['sqlite']
        self.file_format = file_format
        self.out_dir = out_dir

        vars_db_con = sqlite3.connect("data/census_variables.db")

        variables_df = pd.read_sql_query(
            f"SELECT * from census_variables WHERE year = {self.year} AND "
            f"tableid = '{self.table_id}'",
            vars_db_con)

        self.variables_list = [
            f'{i}E' for i in variables_df['uniqueid'].unique()]
        # ToDo Add underscore for years that don't have it.

        census_data = CensusACS5Year(
            self.api_key, self.year, self.out_dir, self.table_id,
            geography=self.geography, variables=self.variables_list)

        census_data.get_data()

        self.df = census_data.df

        table_name = f'{self.year}_5yr_acs_{self.geography}'

        if 'sqlite' in file_format:
            engine = create_engine(
                f'sqlite:///test/{table_name}.db', echo=False)
            census_data.df.to_sql(
                f'{self.table_id}', con=engine, if_exists='replace')

        if 'csv' in file_format:
            census_data.write_data()


if __name__ == '__main__':
    config = read_json('config.json')

    for census_year in [2015, 2016, 2017, 2018, 2019]:
        for census_geog in ['county']:  #, 'tract']:
            for topic in ['B19013', 'B25033']:
                CensusTableRequest(
                    config['api_key'], census_year, census_geog, topic, 'test',
                    ['csv', 'sqlite'])
