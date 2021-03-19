from census import Census
import us
import pandas as pd
from tools.helpers import create_directory, split_list_to_chunks
from tools.helpers import dict_to_json
from tools.census_api_data_dictionary import generate_census_variable_definition
from functools import reduce
import time


class CensusACS5Year:

    def __init__(
            self,
            api_key,
            year,
            out_dir,
            table_name,
            geography='tract',
            variables=None,
            states=us.states.STATES + [us.states.DC],
    ):
        if not variables:
            variables = ["NAME", "B01003_001E"]
        self.api_key = api_key
        self.year = year
        self.table_name = table_name
        self.geog = geography
        self.geog_str = self.geog.replace(' ', '_')
        self.vars = variables
        self.states = states
        self.out_dir = out_dir
        self.census_api = Census(self.api_key, year=self.year)
        self.vars_data = {}
        self.df = None  # added this, should be mutable

    def get_dataframe(self, variables_list, state_obj=None):
        print(variables_list)
        if self.geog in ['tract', 'place']:
            geog_query = {
                'for': f'{self.geog}:*', 'in': f'state:{state_obj.fips}'}

        elif self.geog in ['zip code tabulation area', 'state', 'county']:
            geog_query = {'for': f'{self.geog}:*'}

        else:  # ToDo - not sure if this is good, but do need to declare query
            geog_query = {'for': f'{self.geog}:*'}

        split_vars = split_list_to_chunks(variables_list, 49)  # 50 is api limit
        print(print(type(split_vars), split_vars))

        df_list = []

        for vs in split_vars:
            df = pd.DataFrame(self.census_api.acs5.get(vs, geo=geog_query))

            if self.geog in ['zip code tabulation area', 'state']:
                df['geoid'] = df[self.geog]

            elif self.geog == 'county':
                df['geoid'] = df['state'].astype(str) + \
                              df['county'].astype(str)

            elif self.geog == 'tract':
                df['geoid'] = df['state'].astype(str) + \
                              df['county'].astype(str) + \
                              df['tract'].astype(str)

            elif self.geog == 'place':
                df['geoid'] = df['state'].astype(str) + \
                              df['place'].astype(str)

            df.drop(['state', 'place', 'zip code tabulation area', 'county',
                     'tract'], axis=1, errors='ignore', inplace=True)

            df_list.append(df)

        df = reduce(
            lambda x, y: pd.merge(x, y, on='geoid', how='outer'), df_list)

        # df = df.loc[:, ~df.columns.duplicated()]  # remove duplicated id

        return df

    def get_data(self):
        if self.geog in ['zip code tabulation area', 'county', 'state']:
            self.df = self.get_dataframe(self.vars)

        elif self.geog in ['tract', 'place']:
            self.df = pd.concat([
                self.get_dataframe(
                    self.vars, state_obj=s) for s in self.states])

    def write_data(self):
        create_directory(self.out_dir)
        self.df.to_csv(
            f'{self.out_dir}/{self.year}_5yr_acs_{self.geog_str}_'
            f'{self.table_name}.csv', index=False)

    def get_data_dictionary(self):
        for variable in self.vars:
            self.vars_data[variable] = generate_census_variable_definition(
                variable, self.year)

            time.sleep(0.5)

    def write_data_dictionary(self):
        dict_to_json(self.vars_data, f'{self.out_dir}/acs_{self.geog_str}.json')
