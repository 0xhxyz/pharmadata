import csv
import json
import requests
from bs4 import BeautifulSoup
import os

if not os.path.exists('csv'):
    os.makedirs('csv')

if not os.path.exists('json'):
    os.makedirs('json')

url = 'http://www.dpm.tn/dpm_pharm/medicament/listpays.php'


def get_countries():

    country_unselected = requests.post(url)

    if country_unselected.status_code == 200:
        print('Request successful!')
    else:
        print(
            f'Request failed with status code {country_unselected.status_code}'
        )

    soup = BeautifulSoup(country_unselected.content, 'html.parser')

    select_tag = soup.find('select', {'name': 'cod_pays'})

    country_codes = []

    for option in select_tag.find_all('option'):
        value = option['value']
        country_codes.append(value)

    country_codes.remove(country_codes[0])
    return country_codes


def parse_countries(url, countries):

    for country in countries:

        data = {'cod_pays': f'{country}', 'CHERCHER': 'Continuer'}

        response = requests.post(url, data=data)

        soup = BeautifulSoup(response.content, 'html.parser')

        parse_laboratories_csv(soup, country)
        parse_laboratories_json(soup, country)




def parse_laboratories_csv(soup, country):
    table = soup.find('table')

    rows = []

    for tr in table.find_all('tr'):

        row = []

        for td in tr.find_all('td'):

            cell_text = td.get_text(strip=True)
            row.append(cell_text)

        rows.append(row)

    csv_filename = f"{country}.csv"

    with open("csv/" + csv_filename, 'w', newline='',
              encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)

        for row in rows:
            csvwriter.writerow(row)

        print(f"Success making csv for {country}")




def parse_laboratories_json(soup, country):
    table = soup.find('table')

    data = []
    start = True

    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        data.append({
            'LABORATOIRE': cols[0].get_text(strip=True),
            'ADRESSE': cols[1].get_text(strip=True),
            'TEL': cols[2].get_text(strip=True),
            'FAX': cols[3].get_text(strip=True),
        })

        # print(data)

    json_filename = f"{country}.json"

    with open("json/" + json_filename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=4)

    print(f"Success making json for {country}")


cod_pays = get_countries()

parse_countries(url, cod_pays)
