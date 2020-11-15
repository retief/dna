import sys
from Bio import Entrez
from api.genome import genome_file_path

genome = sys.argv[1]
with Entrez.efetch(db="nuccore", id=genome, rettype="gb", retmode="xml") as handle:
    with open(genome_file_path(genome), "wb") as f:
        f.write(handle.read())
