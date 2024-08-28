import requests

class DataService:
    def __init__(self):
        self.base_url = 'https://www.datos.gov.co/resource/xdk5-pm3f.json'

    def fetch_departamentos(self):
        try:
            response = requests.get(self.base_url)
            if response.status_code == 200:
                data = response.json()
                departamentos_set = set()
                for element in data:
                    departamentos_set.add(element['departamento'])
                departamentos_list = list(departamentos_set)
                return departamentos_list
            else:
                raise Exception('Failed to load departamentos')
        except Exception as e:
            raise Exception(f'Error: {e}')

    def fetch_municipios(self, departamento):
        try:
            url = f'{self.base_url}?departamento={departamento}'
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                municipios_list = [e['municipio'] for e in data]
                return municipios_list
            else:
                raise Exception('Failed to load municipios')
        except Exception as e:
            raise Exception(f'Error: {e}')
