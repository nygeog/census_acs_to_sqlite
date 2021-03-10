from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import glob
import os


class CreateTableShellDatabase:
    def __init__(self, db_name, table_shells_dir='../data/table_shells'):
        engine = create_engine(db_name, echo=False)

        filenames = glob.glob(f'{table_shells_dir}/*.xls*')

        variables_df_list, tables_df_list = [], []

        for f in filenames:
            year = os.path.basename(f)[3:7]
            if year == '2013':  # sheet name exception for this year
                df = pd.read_excel(f, sheet_name='Sheet2')
            elif year == '2014':  # sheet name exception for this year
                df = pd.read_excel(f, sheet_name='Sheet4')
            else:
                df = pd.read_excel(f)

            df.columns = [
                i.replace('\n', '_').replace(' ', '').replace('_', '').lower()
                for i in df.columns]

            df.replace(r'^\s*$', np.nan, regex=True, inplace=True)
            df.dropna(how='all', inplace=True)

            df['year'] = year

            df = df[['tableid', 'uniqueid', 'stub', 'year']]

            df_tables = df[df['uniqueid'].isnull()]

            df_tables = df_tables.groupby(['tableid', 'year'])['stub'].apply(
                ' - '.join).reset_index()

            tables_df_list.append(df_tables)

            df_variables = df[df['uniqueid'].notnull()]

            variables_df_list.append(df_variables)

        df_variables = pd.concat(variables_df_list)
        df_tables = pd.concat(tables_df_list)

        df_variables.to_sql(
            f'census_variables', con=engine, if_exists='replace')

        df_tables.to_sql(
            f'census_tables', con=engine, if_exists='replace')


if __name__ == '__main__':
    CreateTableShellDatabase(
        'sqlite:///../data/census_variables.db')
