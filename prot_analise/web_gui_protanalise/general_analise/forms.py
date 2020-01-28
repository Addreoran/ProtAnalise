from django import forms

from .models import Database


class GetData(forms.Form):
    try:
        database = Database.objects.get(name="UniprotKB")
    except:
        database = Database()
        database.name = "UniprotKB"
        database.save()
    database = forms.ModelChoiceField(
        queryset=Database.objects.all(),
        to_field_name='name',
    )

    cluster_header = forms.CharField(widget=forms.Textarea,
                                     initial=">c;\(.*\)\\r\\n")
    data = forms.CharField(widget=forms.Textarea,
                           initial=">c;('H',)\r\n"
                                   ">s;id=11;uniprot_id=Q9LUV4;beg=515;end=529;family=Frigida family\r\n"
                                   "HPHHHQHHQFHHQQH\r\n"
                                   ">s;id=16;uniprot_id=P32242;beg=291;end=300;family=paired homeobox"
                                   " family Bicoid subfamily\r\n"
                                   "HHHHHHHHHH\r\n"
                                   ">s;id=2214;uniprot_id=P11048;beg=558;end=567;family=intermediate filament "
                                   "family\r\n"
                                   "HHHHHHHHHH\r\n"
                                   ">s;id=4682;uniprot_id=P49639;beg=64;end=73;family=Antp homeobox family Labial "
                                   "subfamily\r\n"
                                   "HHHHHHHHHH\r\n"
                                   ">s;id=26;uniprot_id=P23091;beg=168;end=198;family=bZIP family Maf subfamily\r\n"
                                   "GGAPHYHHHHHHPHHGGGGGGGGHPHGAAPG")

    def send_data(self):
        return self.data
