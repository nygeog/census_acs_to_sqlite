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
            self, api_key, year, geography, table_id, out_dir, file_formats=None
    ):
        self.api_key = api_key
        self.year = year
        self.geography = geography
        self.table_id = table_id
        if file_formats is None:
            file_formats = ['sqlite']
        self.file_formats = file_formats
        self.out_dir = out_dir

        vars_db_con = sqlite3.connect("data/census_variables.db")

        variables_df = pd.read_sql_query(
            f"SELECT * from census_variables WHERE year = {self.year} AND "
            f"tableid = '{self.table_id}'",
            vars_db_con)

        self.variables_list = [
            f'{i}E' for i in variables_df['uniqueid'].unique()]
        self.variables_list = [i if '_' in i else i[:6] + '_' + i[6:]
                               for i in self.variables_list]
        # ToDo Add underscore for years that don't have it.

        census_data = CensusACS5Year(
            self.api_key, self.year, self.out_dir, self.table_id,
            geography=self.geography, variables=self.variables_list)

        census_data.get_data()

        self.df = census_data.df

        table_name = f'{self.year}_5yr_acs_{self.geography}'

        if 'sqlite' in file_formats:
            engine = create_engine(
                f'sqlite:///{self.out_dir}/{table_name}.db', echo=False)
            census_data.df.to_sql(
                f'{self.table_id}', con=engine, if_exists='replace')

        if 'csv' in file_formats:
            census_data.write_data()


if __name__ == '__main__':
    config = read_json('config.json')

    # 2015, 2016, 2017,
    for census_year in [2018]: #, 2019]:
        for census_geog in ['county']:  # state', 'tract']:  # 'county 'tract'  # ToDo - state and tract work, why not county?
            for topic in ['B05001']:  # B01001', 'B19013', 'B25033',
                CensusTableRequest(
                    config['api_key'], census_year, census_geog, topic,
                    'data/output',
                    ['csv', 'sqlite'])
