import requests


def generate_census_variable_definition(variable, year):
    api_prefix = 'https://api.census.gov/data'
    url = f'{api_prefix}/{year}/acs/acs5/variables/{variable}.json'
    r = requests.get(url).json()
    r['link'] = url
    r['link_text'] = f'Accessed from {url}.'
    return r
