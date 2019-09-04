import requests
from multiprocessing.pool import Pool

from prot_analise.scripts.parse_XML import ParseXML
from prot_analise.scripts.region import Region


class AllData:
    def __init__(self):
        self.proteins = {}
        self.species = {}
        self.cells = {}
        self.path = ""
        self.lenths = {}
        self.kingdom = {}
        self.logs = {}
        self.loaded_protein = ""
        self.popularity = []

    def get_region_by_seq(self, list_prot, seq, begin, end):
        for sequence in list_prot:
            if sequence.get_sequence() == seq and sequence.get_begin() == begin and sequence.get_end() == end:
                return sequence

    def get_path(self, path):
        self.proteins = {}
        self.path = path
        f = open(path, 'r')
        uniprotid = None
        seq_reg = ""
        begin = 0
        end = 0

        for i in f.readlines():
            if i != "":
                if i.startswith(">s"):
                    if uniprotid:
                        if uniprotid not in self.proteins.keys():
                            self.proteins[uniprotid] = [Region(uniprotid, seq_reg, begin, end)]
                        else:
                            if not self.get_region_by_seq(self.proteins[uniprotid], seq_reg, begin, end):
                                self.proteins[uniprotid].append(Region(uniprotid, seq_reg, begin, end))
                    uniprotid = i.split(";")[2].split("=")[1]
                    seq_reg = ""
                    begin = i.split(";")[3].split("=")[1]
                    end = i.split(";")[4].split("=")[1]
                    print("uniprotId ", uniprotid)
                    print("seq ", seq_reg)
                    print("begin ", begin)
                    print("end ", end)
                elif uniprotid and not i.startswith(">"):
                    seq_reg += i.strip()
        if uniprotid:
            if uniprotid not in self.proteins.keys():
                self.proteins[uniprotid] = [Region(uniprotid, seq_reg, begin, end)]
            else:
                if not self.get_region_by_seq(self.proteins[uniprotid], seq_reg, begin, end):
                    self.proteins[uniprotid].append(Region(uniprotid, seq_reg, begin, end))
        self.loaded_protein = ""

    def get_data_database(self, path):
        parser = ParseXML(path, True)
        parser.parse_onefile_XMLs(self.proteins.keys())
        self.lenths = parser.get_lenths()
        self.kingdom = parser.kingdoms
        self.species = parser.specieses
        self.lenths = parser.lenths
        print("get data", self.species)

    def get_group_taxonomy(self):
        missing = []
        p = Pool(8)
        res = p.map(parse_uniprot, list(self.proteins.keys()))
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
        print(self.lenths)
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
            self.lenths[protein] = length
            return True
        else:
            return False

    def search_popularity(self):
        self.popularity = []
        names = []
        for i in range(0, 101):
            self.popularity.append([])
            names.append(i)
        for i in self.proteins.items():
            for region in i[1]:
                begin = int(100 * round(int(region.get_begin()) / self.lenths[i[0]], 2))
                end = int(100 * round(int(region.get_end()) / self.lenths[i[0]], 2))
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
        for id in data_set:
            for region in self.proteins[id]:
                text += ">protein = " + region.uniprot_id + " "
                text += "begin = " + str(region.get_begin()) + " "
                text += "end = " + str(region.get_end()) + " \n"
                text += str(region.sequence) + "\n"
        return text


def parse_uniprot(protein):
    try:
        link = 'https://www.uniprot.org/uniprot/' + str(protein) + ".xml"
        r = requests.request('GET', link)
        dane_all = r.text  # .decode('utf-8')
        print(protein, " ", link)
        data = ParseXML(dane_all)
        lenth, taxonomy, protein_xml, species = data.parse_XML()
        return lenth, taxonomy, protein_xml, species, protein
    except:
        return [], [], [], [], protein
