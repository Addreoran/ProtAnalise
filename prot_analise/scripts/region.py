class Region:
    def __init__(self, uniprot_id, sequence, begin, end, header=None):
        self.uniprot_id = uniprot_id
        self.sequence = sequence
        self.begin = begin
        self.end = end
        self.header = header
