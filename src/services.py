import requests
import json
import xml.etree.ElementTree as ET
from datetime import datetime


def search_city(cep):
    api_request = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
    formated_data = json.loads(api_request.content)
    return formated_data['localidade']

def search_city_code(city):
    api_request = requests.get(f'http://servicos.cptec.inpe.br/XML/listaCidades?city={city}')
    root = ET.ElementTree(ET.fromstring(api_request.content))
    id = None
    for child in root.findall("cidade"):
        id = child.find("id").text
        break
    return id

def search_forecast(cep):
    city = search_city(cep)
    id = search_city_code(city)


    api_request = requests.get(f'http://servicos.cptec.inpe.br/XML/cidade/{id}/previsao.xml')
    root = ET.ElementTree(ET.fromstring(api_request.content))
    forecasts = []

    for child in root.findall('previsao'):
        dia = child.find('dia').text
        tempo = child.find('tempo').text
        maxima = child.find('maxima').text
        minima = child.find('minima').text
        iuv = child.find('iuv').text

        new_forecast_obj = {"day": dia, "weather": tempo, "max": maxima, "min": minima, 'iuv': iuv}
        forecasts.append(new_forecast_obj)
    return forecasts

def gen_logs(code, method, input, output, message):
    now = datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    new_log = {"request_time": str(now), "status_code": code, "methods": method, "input": input, "output": output,  "message": message}
    headers = {'Content-Type': 'application/json'}

    formatted_data = json.dumps(new_log)
    requests.post('http://elasticsearch:9200/logs/_doc', data=formatted_data, headers=headers)