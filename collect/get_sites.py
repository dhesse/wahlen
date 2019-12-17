from bs4 import BeautifulSoup
import requests
import yaml

base_url = 'https://www.wahlrecht.de/umfragen'

def get_sites():
    soup = BeautifulSoup(requests.get(f'{base_url}/index.htm').text,
                         features="html.parser")
    sites = []
    for h in soup('th'):
        link = h.find('a')
        if link:
            sites.append({'url': f"{base_url}/{link['href']}",
                          'name': link.text})
    return sites

if __name__ == '__main__':
    with open('sites.yaml', 'w') as sites_file:
        sites_file.write(yaml.dump(get_sites()))
