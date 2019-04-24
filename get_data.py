import requests
import json
import codecs
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from typing import List


class GetData:
    """A class to get data from a specific local authority"""

    def __init__(self, authority_name=None, url='http://api.erg.kcl.ac.uk/AirQuality/'):
        self.authority_name = authority_name.title()
        self.url = url

    def get_local_authority_data(self, url_suffix):
        r = requests.get(self.url + url_suffix)
        data = r.json()['LocalAuthorities']['LocalAuthority']
        if self.authority_name is None:
            pass
        elif self.authority_name is not None:
            for item in data:
                if item['@LocalAuthorityName'] == self.authority_name:
                    data = item
        else:
            print('Please insert a valid name')
        return data

    def get_pollution_data(self, local_authority_id, year):
        url_suffix = '/Annual/MonitoringObjective/LocalAuthorityId={0}/Year={1}/Json'.format(str(local_authority_id),
                                                                                             str(year))
        r = requests.get(self.url + url_suffix)
        json_data = json.loads(codecs.decode(r.content, 'utf-8-sig'))
        pollution_df = pd.DataFrame({'species_code': [], 'species_desc': [],
                                     'objective_name': [], 'value': [],
                                     'site_name': [],
                                     'year': []})
        try:
            for item in json_data['SiteObjectives']['Site']:
                for part in item['Objective']:
                    pollution_df = pollution_df.append({'species_code': part['@SpeciesCode'],
                                                        'species_desc': part['@SpeciesDescription'],
                                                        'objective_name': part['@ObjectiveName'],
                                                        'value': part['@Value'],
                                                        'site_name': item['@SiteName'],
                                                        'year': part['@Year']}, ignore_index=True)
        except TypeError:
            list_data = json_data['SiteObjectives']['Site']
            for item in list_data['Objective']:
                pollution_df = pollution_df.append({'species_code': item['@SpeciesCode'],
                                                    'species_desc': item['@SpeciesDescription'],
                                                    'objective_name': item['@ObjectiveName'],
                                                    'value': item['@Value'],
                                                    'site_name': list_data['@SiteName'],
                                                    'year': item['@Year']}, ignore_index=True)
        return pollution_df

    @staticmethod
    def plot_pollution_by_species(species, data_list: List):
        df_species = pd.DataFrame()
        for df in data_list:
            df_species = df_species.append(
                df.loc[(df['species_code'] == species) & (df['objective_name'] == 'Capture Rate (%)')])
        df_species['value'] = df_species['value'].apply(pd.to_numeric)
        plt.figure(figsize=(16, 6))
        g = sns.lineplot(x="year", y="value", hue="site_name", data=df_species, marker="o")
