class Region:
    def __init__(self, uniprot_id, sequence, begin, end, header=None):
        self.uniprot_id = uniprot_id
        self.sequence = sequence
        self.begin = begin
        self.end = end
        self.header = header

    def set_header(self, header):
        self.header = header

    def get_normalised_location(self):
        pass

    def get_begin(self):
        return self.begin

    def get_end(self):
        return self.end

    def get_sequence(self):
        return self.sequence
