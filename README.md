# ProtAnalise

The project ProtAnalise aims to facilitate the analysis of protein fragments. A quick look at the set of proteins from which comes regions can have a key impact on reducing the number of subsequent analyzes.

## Getting Started

Input file should have set of regions in fasta file. Headers of regions should look like:
```angular2html
>s;id=[...];uniprot_id=[...];beg=[...];end=[...];[...]
```

Other formats of headers are not implemented jet.

###Example

To start using ProtAnalise, install all requirements and run.

```angular2html
python3 ./prot_analise/gui/ProtAnalise.py
```

In tab Load File you can load data from example file ./prot_analise_examples/clustry_H.csv. To download more data about proteins from which comes fragments click "Download data from UniprotKB". 
Finally, you can see your data in tab Data. Choose a category from second combo list and analyze them as you want.

It is also possible to change your data in this tab and saving them in memory of ProtAnaliser. During my development of this program, you will also save changed data and make more analysis. 
 