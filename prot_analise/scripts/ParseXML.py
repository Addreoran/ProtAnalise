import io

from bs4 import BeautifulSoup


class ParseXML:
    def __init__(self, data):
        self.soup = self.identify_input(data)

        self.kingdom = str()
        self.lenght = int()
        self.name = str()
        self.species = str()
        self.kingdoms = {}
        self.lenths = {}
        self.specieses = {}

    def parse_onefile_XMLs(self):
        # print(soup)
        entries = self.soup.find_all("entry")
        for i in entries:
            self.parse_XML(i)

            if self.kingdom not in self.kingdoms.keys():
                self.kingdoms[self.kingdom] = [self.name]
            else:
                self.kingdoms[self.kingdom].append(self.name)
            if self.species not in self.specieses.keys():
                self.specieses[self.species] = [str(i)]
            else:
                self.specieses[self.species].append(str(i))
            self.lenths[self.name] = self.lenght

    def identify_input(self, data):
        if data.__class__ == BeautifulSoup:
            soup = data
        elif data.__class__ == str:
            soup = BeautifulSoup(data, 'html.parser')
        elif data.__class__ == io.TextIOWrapper:
            soup = BeautifulSoup(open(data).read(), 'html.parser')
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

        self.lenths = int(soup.find("sequence", length=True)['length'])
        return self.lenght, self.kingdom, self.name, self.species
