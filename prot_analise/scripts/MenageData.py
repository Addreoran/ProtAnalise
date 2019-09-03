import requests
from multiprocess.pool import Pool

from scripts.ParseXML import ParseXML
from scripts.Region import Region


class AllData():
    def __init__(self):
        self.proteins = {}
        self.species = {}
        self.cells = {}
        self.path = ""
        self.lenths = {}
        self.kingdom = {}
        self.logs = {}
        self.loaded_protein = ""

    def get_region_by_seq(self, list_prot, seq, begin, end):
        for sequence in list_prot:
            if sequence.get_sequence() == seq and sequence.get_begin() == begin and sequence.get_end() == end:
                return sequence

    def get_path(self, path):
        self.proteins = {}
        self.path=path
        f = open(path, 'r')
        uniprotid=None
        seq_reg = ""
        begin = 0
        end = 0

        for i in f.readlines():
            if i != "":
                if i.startswith(">s"):
                    # seq = 1
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


                #                 >s;id=16;uniprot_id=P32242;beg=291;end=300;family=paired homeobox family Bicoid subfami
                elif uniprotid and not i.startswith(">"):
                    seq_reg += i.strip()


        if uniprotid:
            if uniprotid not in self.proteins.keys():
                self.proteins[uniprotid] = [Region(uniprotid, seq_reg, begin, end)]
            else:
                if not self.get_region_by_seq(self.proteins[uniprotid], seq_reg, begin, end):
                    self.proteins[uniprotid].append(Region(uniprotid, seq_reg, begin, end))

        self.loaded_protein = ""

    def get_group_taxonomy(self):
        print(len(self.proteins.keys()))
        missing = []
        p = Pool(8)
        res = p.map(parse_uniprot, list(self.proteins.keys()))

        for date in res:
            print(date)
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





    # def load_datas(self):
    #     self.get_path(self.path)

    def search_cellularity(self):
        pass

    def search_secretion(self):
        pass

    def search_place_activity(self):
        pass



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

