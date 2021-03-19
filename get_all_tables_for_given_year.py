from census_acs_to_sqlite import CensusTableRequest
from tools.helpers import read_json
import sqlite3
import pandas as pd


if __name__ == '__main__':
    config = read_json('config.json')

    not_collected = {}

    # 2015, 2016, 2017,
    for census_year in [2018]:  # 2019 done
        for census_geog in ['zip code tabulation area']:  # 'state'

            not_collected[census_year] = {}
            not_collected[census_year][census_geog] = {}

            vars_db_con = sqlite3.connect("data/census_variables.db")

            tables_df = pd.read_sql_query(
                f"SELECT * from census_tables WHERE year = {census_year}",
                vars_db_con)

            # ToDo - grab all topics from the db for a given year
            tableid_list = [
                i for i in tables_df['tableid'].unique()]

            for tableid in tableid_list:

                # ToDo - maybe skip ones with extra letters at the end like B01001B
                # ToDo - like just collect B01001, not B01001B, B01001C, B01001H
                print(tableid)

                # noinspection PyBroadException
                try:
                    CensusTableRequest(
                        config['api_key'], census_year, census_geog, tableid,
                        'data/output',
                        ['sqlite'])

                except Exception as e:
                    not_collected[census_year][census_geog][tableid] = []
