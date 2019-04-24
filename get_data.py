import requests
import json
import codecs
import pandas as pd


class GetData:
    """A class to get data from a specific local authority"""

    def __init__(self, authority_name=None, url='http://api.erg.kcl.ac.uk/AirQuality/'):
        self.authority_name = authority_name.title()
        self.url = url

    def get_local_authority_data(self, url_suffix):
        r = requests.get(self.url + url_suffix)
        data = r.json()['LocalAuthorities']['LocalAuthority']
        if self.authority_name == None:
            pass
        elif self.authority_name != None:
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
                                     'site_name': []})
        for item in json_data['SiteObjectives']['Site']:
            for part in item['Objective']:
                pollution_df = pollution_df.append({'species_code': part['@SpeciesCode'],
                                                    'species_desc': part['@SpeciesDescription'],
                                                    'objective_name': part['@ObjectiveName'],
                                                    'value': part['@Value'],
                                                    'site_name': item['@SiteName']},
                                                   ignore_index=True)

        return pollution_df
