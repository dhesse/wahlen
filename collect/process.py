from metaflow import FlowSpec, Flow, metadata, step
from bs4 import BeautifulSoup

from get_data import get_header
from transformers import transform


def process_rows(header, table):
    body = table.find("tbody")
    return [
        {h: td.text for h, td in zip(header, tr.find_all("td")) if td.text != "\xa0"}
        for tr in body.find_all("tr")
    ]


class ProcessData(FlowSpec):
    @step
    def start(self):
        self.sites = Flow("DownloadData").latest_successful_run.data.sites
        self.next(self.extract_tables, foreach="sites")

    @step
    def extract_tables(self):
        soup = BeautifulSoup(self.input["text"], "html.parser")
        table = soup.find("table", {"class": "wilko"})
        parties = get_header(table)
        parties[0] = "Date"
        self.site_name = self.input["name"]
        self.raw_data = process_rows(parties, table)
        self.next(self.discard_invalid)
    
    @step
    def discard_invalid(self):
        correct_length = len(self.raw_data[0])
        self.raw_data = list(filter(lambda r: len(r) == correct_length, self.raw_data))
        self.next(self.parse)
    
    @step
    def parse(self):
        self.parsed_data = [{k: transform(row[k]) for k in row} for row in self.raw_data]
        self.next(self.join)
    
    @step
    def join(self, inputs):
        self.parsed_sites = {input.site_name: input.parsed_data for input in inputs}
        self.next(self.end)
    
    @step
    def end(self):
        pass

if __name__ == "__main__":
    ProcessData()