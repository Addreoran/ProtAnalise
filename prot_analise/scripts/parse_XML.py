import io
import os

import bs4
from bs4 import BeautifulSoup


class ParseXML:
    def __init__(self, data, typ=False):
        self.typ = typ

        self.soup = self.identify_input(data)

        self.kingdom = str()
        self.lenght = int()
        self.name = str()
        self.species = str()
        self.kingdoms = {}
        self.lengths = {}
        self.specieses = {}

    def parse_onefile_XMLs(self, uniprot_ids):
        text = ""
        # todo: it desn't works properly
        import gc
        gc.set_debug(gc.DEBUG_SAVEALL)
        if int(os.stat(self.soup).st_size) < 10000000.0:
            file = open(self.soup)
            entries = BeautifulSoup(file.read(), 'html.parser').find_all("entry")
            file.close()
            for entry in entries:
                if entry.find("accession").text in list(uniprot_ids):
                    lenght, kingdom, name, species = self.parse_XML(entry)

                    if kingdom not in self.kingdoms.keys():
                        self.kingdoms[kingdom] = [name]
                    else:
                        self.kingdoms[kingdom].append(name)
                    if species not in self.specieses.keys():
                        self.specieses[species] = [name]
                    else:
                        self.specieses[species].append(name)
                    self.lengths[name] = lenght
        else:
            with open(self.soup) as f:
                line = "pusta"
                while line:
                    gc.collect()
                    line = str(f.readline()).strip()
                    if line.startswith("<entry "):
                        text += line
                    elif text != "" and line != "</entry>":
                        text += line
                    elif line.strip() == "</entry>":
                        text += line
                        entry = BeautifulSoup(text, 'html.parser')
                        if entry.find("accession").text in list(uniprot_ids):
                            lenght, kingdom, name, species = self.parse_XML(entry)

                            if self.kingdom not in self.kingdoms.keys():
                                self.kingdoms[kingdom] = [name]
                            else:
                                self.kingdoms[kingdom].append(name)
                            if self.species not in self.specieses.keys():
                                self.specieses[species] = [name]
                            else:
                                self.specieses[species].append(name)
                            self.lengths[name] = lenght
                        text = ""

    def identify_input(self, data):
        if isinstance(data, BeautifulSoup) or isinstance(data, bs4.element.Tag):
            soup = data
        elif self.typ:
            soup = data
        elif isinstance(data, str) and data[-4:] != ".xml":
            soup = BeautifulSoup(data, 'html.parser')
        elif isinstance(data, io.TextIOWrapper):
            soup = BeautifulSoup(data.read(), 'html.parser')
        else:
            raise Exception("Wrong format in XML parser.")
        return soup

    def get_kingdoms(self):
        return self.kingdoms

    def get_lengths(self):
        return self.lengths

    def parse_XML(self, text=None):
        if text:
            soup = self.identify_input(text)
        else:
            soup = self.soup
        species = soup.find("organism").find("name", type="scientific").text
        lineage = soup.find_all("taxon")
        name = soup.find("accession").text
        if lineage[0].text == "Eukaryota":
            kingdom = lineage[1].text
        else:
            kingdom = lineage[0].text

        lenght = int(soup.find("sequence", length=True)['length'])
        return lenght, kingdom, name, species
