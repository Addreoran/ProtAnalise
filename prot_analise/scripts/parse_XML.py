import io

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
        self.lenths = {}
        self.specieses = {}

    def parse_onefile_XMLs(self, uniprot_ids):
        text = ""
        with open(self.soup) as f:
            line="pusta"
            while line:
                line = str(f.readline())

                if line.startswith("<entry "):
                    text += line
                elif text != "" and line !="</entry>":
                    text += line
                    # print(text)
                elif line == "</entry>":
                    # print(text)
                    entry = BeautifulSoup(text, 'html.parser')
                    # print("accesion",entry.find("accession"))
                    if entry.find("accession").text in list(uniprot_ids):
                        self.parse_XML(entry)

                        if self.kingdom not in self.kingdoms.keys():
                            self.kingdoms[self.kingdom] = [self.name]
                        else:
                            self.kingdoms[self.kingdom].append(self.name)
                        if self.species not in self.specieses.keys():
                            self.specieses[self.species] = [self.name]
                        else:
                            self.specieses[self.species].append(self.name)
                        self.lenths[self.name] = self.lenght
                    text = ""


    def identify_input(self, data):
        # print(data[:-4])
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

    def get_lenths(self):
        return self.lenths

    def parse_XML(self, text=None):
        if text:
            soup = self.identify_input(text)
        else:
            soup = self.soup
        self.species = soup.find("organism").find("name", type="scientific").text
        lineage = soup.find_all("taxon")
        self.name = soup.find("accession").text
        if lineage[0].text == "Eukaryota":
            self.kingdom = lineage[1].text
        else:
            self.kingdom = lineage[0].text

        self.lenght = int(soup.find("sequence", length=True)['length'])
        return self.lenght, self.kingdom, self.name, self.species
