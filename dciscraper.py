import requests
from bs4 import BeautifulSoup

url = 'http://www.dpm.tn/dpm_pharm/medicament/dci.php'


def get_dci():

    dcireq = requests.post(url)

    if dcireq.status_code == 200:
        print('Request successful!')
    else:
        print(
            f'Request failed with status code {dcireq.status_code}'
        )

    soup = BeautifulSoup(dcireq.content, 'html.parser')

    table = soup.find('table')

    rows = []


    with open("dci.txt", 'w') as f:
        for tr in table.find_all('tr')[1:]:

            td = tr.find('td')
            cell_text = td.get_text(strip=True)
            f.write(cell_text + "\n")



dci = get_dci()

