import csv
import logging 

from packaging import version
from tqdm import tqdm
from src.html_table_parser import HTMLTableParser, HTMLResponseException


class DependencyTree:
    # versions and packages connected by the index
    # - packages[i] contains package name
    # - versions[i] contains package actual version
    versions: list[str]
    packages: list[str]
    pkg_levels_list: list
    level: int # index for pkg_levels_list, indicates dependency depth level
    hp: HTMLTableParser

    def __init__(self, source_fname: str) -> None:
        self.versions = []
        self.packages = []
        self.pkg_levels_list = []
        self.level = 0
        self.hp = HTMLTableParser()

        with open(source_fname) as file:
            packages = csv.reader(file, delimiter=' ')
            for row in packages:
                self.packages.append(row[0])
                self.versions.append(row[1])
            self.pkg_levels_list = []
            self.pkg_levels_list.append([])
            self.pkg_levels_list[0].extend(self.packages)
    
    def parse_dependencies(self):
        while True:
            if self._get_num_level_packages() == 0:
                break
            logging.info(f"Parsing dependencies at {self.level} level")
            for pkg in tqdm(self.pkg_levels_list[self.level]):
                self._process_package(pkg)
            self.level += 1

    def save_results(self, fname_out):
        with open(fname_out, "w") as file:
            writer = csv.writer(file, delimiter=" ")
            for ind, pkg_name in enumerate(self.packages):
                writer.writerow([pkg_name, self.versions[ind]])

    def _get_num_level_packages(self):
        if len(self.pkg_levels_list) == self.level:
            self.pkg_levels_list.append([])
            return 0
        return len(self.pkg_levels_list[self.level])

    def _process_package(self, pkg_name: str):
        try:
            pkg_depts = self.hp.parse_depths(pkg_name)
        except HTMLResponseException:
            return
        self._update_depts(pkg_depts["dependencies"])
    
    def _update_depts(self, depts):
        for pkg in depts:
            if pkg.name not in self.packages:
                self.packages.append(pkg.name)
                self.versions.append(pkg.version)
                self._extend_level_list(self.level + 1, pkg.name)
            else:
                pkg_verion_index = self.packages.index(pkg.name)
                if self.versions[pkg_verion_index] == "latest":
                    self.versions[pkg_verion_index] = pkg.version
                elif pkg.version == "latest":
                    return
                else:
                    self.versions[pkg_verion_index] = max([pkg.version, self.versions[pkg_verion_index]], key=version.parse)

    def _extend_level_list(self, level: int, pkg_name: str):
        if len(self.pkg_levels_list) == level:
            self.pkg_levels_list.append([])
        self.pkg_levels_list[level].append(pkg_name)