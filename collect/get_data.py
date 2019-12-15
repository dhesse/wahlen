import gzip
import json
import re

import requests
import yaml
from bs4 import BeautifulSoup


def parse_sites(sites):
    data = {}
    for site in sites:
        data[site["name"]] = parse_site(site)
    return data


def get_header(table):
    header = table.find("thead")
    return [th.text for th in header.find("tr").find_all("th")]


def process_data(text):
    digit_match = re.match(r"(\d+,\d+) \%", text)
    if digit_match:
        return float(digit_match.group(1).replace(",", "."))
    return text


def process_rows(header, table):
    body = table.find("tbody")
    return [
        {
            h: process_data(td.text)
            for h, td in zip(header, tr.find_all("td"))
            if td.text != "\xa0"
        }
        for tr in body.find_all("tr")
    ]


def parse_site(site):
    text = requests.get(site["url"]).text
    soup = BeautifulSoup(text, "html.parser")
    table = soup.find("table", {"class": "wilko"})
    parties = get_header(table)
    parties[0] = "Date"
    return process_rows(parties, table)


if __name__ == "__main__":
    with gzip.open("data/data.json.gz", "w") as data_file:
        with open("collect/sites.yaml") as yaml_file:
            sites = yaml.load(yaml_file)
            data_file.write(json.dumps(parse_sites(sites)))
