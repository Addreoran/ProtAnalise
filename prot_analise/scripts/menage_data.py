import multiprocessing

import requests

from prot_analise.scripts.parse_XML import ParseXML
from prot_analise.scripts.region import Region


class AllData:
    def __init__(self):
        self.proteins = {}
        self.species = {}
        self.cells = {}
        self.path = ""
        self.lengths = {}
        self.kingdom = {}
        self.logs = {}
        self.loaded_protein = ""
        self.popularity = []

    def get_path(self, path):
        self.clear()
        self.path = path
        f = open(path, 'r')
        uniprot_id = None
        seq_reg = ""
        begin = 0
        end = 0

        for line in f.readlines():
            if line != "":
                if line.startswith(">s"):
                    if uniprot_id:
                        if uniprot_id not in self.proteins.keys():
                            self.proteins[uniprot_id] = [Region(uniprot_id, seq_reg, begin, end)]
                        else:
                            if not self.get_region_by_seq(self.proteins[uniprot_id], seq_reg, begin, end):
                                self.proteins[uniprot_id].append(Region(uniprot_id, seq_reg, begin, end))
                    uniprot_id = line.split(";")[2].split("=")[1]
                    begin = line.split(";")[3].split("=")[1]
                    end = line.split(";")[4].split("=")[1]
                    print(uniprot_id, seq_reg, begin, end, sep=", ")
                    seq_reg = ""
                elif uniprot_id and not line.startswith(">"):
                    seq_reg += line.strip()
        if uniprot_id:
            if uniprot_id not in self.proteins.keys():
                self.proteins[uniprot_id] = [Region(uniprot_id, seq_reg, begin, end)]
            else:
                if not self.get_region_by_seq(self.proteins[uniprot_id], seq_reg, begin, end):
                    self.proteins[uniprot_id].append(Region(uniprot_id, seq_reg, begin, end))
        self.loaded_protein = ""

    def get_region_by_seq(self, list_prot, seq, begin, end):
        for sequence in list_prot:
            if sequence.get_sequence() == seq and sequence.begin == begin and sequence.end == end:
                return sequence

    def get_data_database(self, path):
        # todo: improve implementation
        parser = ParseXML(path, True)
        parser.parse_onefile_XMLs(self.proteins.keys())
        self.lengths = parser.get_lengths()
        self.kingdom = parser.kingdoms
        self.species = parser.specieses
        self.lengths = parser.lengths
        print("get data", self.species)

    def get_group_taxonomy(self):
        missing = []
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        res = pool.map(parse_uniprot, list(self.proteins.keys()))
        for date in res:
            if not self.set_prot_info(date):
                missing.append(date[4])
        tmp = missing
        len_miss = len(tmp)
        missing = []
        while len(missing) != len_miss:
            # todo: check it
            tmp = missing
            len_miss = len(tmp)
            missing = []
            for i in tmp:
                result = parse_uniprot(i)
                if not self.set_prot_info(result):
                    missing.append(i)
        self.logs['uniprot_error'] = missing
        print(self.lengths)
        return missing

    def set_prot_info(self, res):
        if res[0] != []:
            length = res[0]
            kingdom = res[1]
            species = res[3]
            protein = res[4]
            if kingdom not in self.kingdom.keys():
                self.kingdom[kingdom] = [protein]
            else:
                self.kingdom[kingdom].append(protein)
            if species not in self.species.keys():
                self.species[species] = [protein]
            else:
                self.species[species].append(protein)
            self.lengths[protein] = length
            return True
        else:
            return False

    def search_popularity(self):
        self.popularity = []
        for i in range(101):
            self.popularity.append([])
        for uniprot_id in self.proteins.items():
            for region in uniprot_id[1]:
                begin = int(100 * round(int(region.begin) / self.lengths[uniprot_id[0]], 2))
                end = int(100 * round(int(region.end) / self.lengths[uniprot_id[0]], 2))
                for adding in range(begin, end + 1):
                    self.popularity[adding].append(region)

    def get_text(self, category, set):
        text = ""
        if set != "all" and set != "":
            if category == "UniprotId":
                data_set = {set: set}
            elif category == "Species":
                data_set = self.species[set]
            elif category == "Groups of Taxonomy (Cellular)":
                data_set = self.kingdom[set]
            else:
                data_set = self.proteins.keys()
        else:
            data_set = self.proteins.keys()
        for id in data_set:
            for region in self.proteins[id]:
                text += ">protein = " + region.uniprot_id + " "
                text += "begin = " + str(region.begin) + " "
                text += "end = " + str(region.end) + " \n"
                text += str(region.sequence) + "\n"
        return text

    def clear(self):
        self.proteins = {}
        self.species = {}
        self.cells = {}
        self.path = ""
        self.lengths = {}
        self.kingdom = {}
        self.logs = {}
        self.loaded_protein = ""
        self.popularity = []


def parse_uniprot(protein):
    try:
        link = 'https://www.uniprot.org/uniprot/' + str(protein) + ".xml"
        r = requests.request('GET', link)
        dane_all = r.text  # .decode('utf-8')
        print(protein, " ", link)
        data = ParseXML(dane_all)
        length, taxonomy, protein_xml, species = data.parse_XML()
        return length, taxonomy, protein_xml, species, protein
    except Exception:
        return [], [], [], [], protein
