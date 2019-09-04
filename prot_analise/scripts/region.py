class Region:
    def __init__(self, uniprot_id, sequence, begin, end, header=None):
        self.uniprot_id = uniprot_id
        self.sequence = sequence
        self.begin = begin
        self.end = end
        self.header = header

    def __eq__(self, other):
        return all([
            self.uniprot_id == other.uniprot_id,
            self.sequence == other.sequence,
            self.begin == other.begin,
            self.end == other.end,
        ])
