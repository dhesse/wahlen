from metaflow import FlowSpec, Parameter, step
from bs4 import BeautifulSoup
import requests

from get_data import parse_site
from get_sites import get_sites


class ElectionDataFlow(FlowSpec):

    @step
    def start(self):
        self.sites = get_sites()
        self.next(self.parse_site, foreach='sites')
    
    @step
    def parse_site(self):
        self.site_name = self.input['name']
        self.site_data = parse_site(self.input)
        self.next(self.join)
    
    @step
    def join(self, inputs):
        self.data = {input.site_name: input.site_data for input in inputs}
        self.next(self.end)
    
    @step
    def end(self):
        pass

if __name__ == "__main__":
    ElectionDataFlow()