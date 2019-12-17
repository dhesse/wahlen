import requests
from metaflow import FlowSpec, Parameter, step

from get_sites import get_sites


class DownloadData(FlowSpec):
    @step
    def start(self):
        """
        Download site list.
        """
        self.sites = get_sites()
        self.next(self.load_site, foreach="sites")

    @step
    def load_site(self):
        """
        Download invidivual sites.
        """
        self.site_name = self.input["name"]
        response = requests.get(self.input["url"])
        response.encoding = response.apparent_encoding
        self.site_data = response.text
        self.next(self.join)

    @step
    def join(self, inputs):
        """
        Save list of raw sites
        """
        self.sites = [
            {"name": input.site_name, "text": input.site_data} for input in inputs
        ]
        self.next(self.end)

    @step
    def end(self):
        pass


if __name__ == "__main__":
    DownloadData()
