import requests
import logging

from bs4 import BeautifulSoup
from packaging import version
from src.package import Package

class HTMLResponseException(Exception):
    pass

class HTMLTableParser:
    def parse_depths(self, pkg):
        pkg_source_url = f"https://cran.r-project.org/web/packages/{pkg}/index.html"
        response = requests.get(pkg_source_url)
        soup = BeautifulSoup(response.text, 'lxml')
        tables = soup.find_all('table')
        try:
            return self._parse_html_table(tables[0])  
        except IndexError:
            logging.info(f"Package {pkg} is not processed due to parsing error")
            logging.info(f"Package {pkg} is default or not exists")
            raise HTMLResponseException

    def _parse_html_table(self, table):
        rows = table.find_all('td')
        res = {"dependencies": []}
        for ind, row in enumerate(rows):
            if "Version" in row.text:
                res["version"] = rows[ind + 1].text
                continue
            if "Depends" in row.text:
                res["dependencies"].extend(self._parse_packages(rows[ind + 1].text))
                continue
            if "Imports" in row.text:
                res["dependencies"].extend(self._parse_packages(rows[ind + 1].text)[::-1])
                break
        return res

    def _parse_packages(self, pkg_sting: str):
        return [ self._parse_package(pkg) for pkg in pkg_sting.split(",") ]
    
    def _parse_package(self, pkg: str):
        pkg_info = pkg.strip().split(' ')
        pkg_name = pkg_info[0]
        pkg_version = "latest"
        if len(pkg_info) == 3:
            pkg_version = pkg_info[2][:-1]
        return Package(pkg_name, pkg_version)
