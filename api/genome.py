from Bio import Entrez
from collections import namedtuple

GenomeMatch = namedtuple("GenomeMatch", "location feature_location protein_id")


def genome_file_path(genome):
    """Returns the file path (relative to the project root) of the data file for a given genome"""
    return f"genome-data/{genome}.xml"


def contains_location(feature, location, length):
    """See if a given feature overlaps with a sequence with the given length starting at location"""
    interval = feature["GBFeature_intervals"][0]
    start = int(interval["GBInterval_from"])
    end = int(interval["GBInterval_to"])
    # when the location is a complement, start > end so use min and max to ensure I'm checking
    # whether the sequence is in the range correctly
    lower = min(start, end)
    upper = max(start, end)
    return location <= upper and location + length - 1 >= lower


def get_protein_id(quals):
    """Pull out the protein_id from a dict of quals

    returns None if the quals don't include a list of protein ids
    """
    for qual in quals:
        if qual["GBQualifier_name"] == "protein_id":
            return qual["GBQualifier_value"]
    return None


def fetch_genome_data(genome):
    """Opens and reads the data file for a given genome

    returns the data in the form of python dicts
    """
    with open(genome_file_path(genome), "rb") as f:
        return Entrez.read(f)


def search_genome(genome, query):
    """Search genome for a given query string

    Returns a GenomeMatch if a match is found or None otherwise
    """
    record = fetch_genome_data(genome)
    seq = record[0]["GBSeq_sequence"]

    location = seq.find(query)
    if location == -1:
        return None
    # ncbi locations seem to start at index 1, so adjust our location value to follow suit
    location = location + 1

    features = record[0]["GBSeq_feature-table"]
    feature_location = None
    protein_id = None

    for feature in features:
        if feature["GBFeature_key"] != "CDS":
            continue

        if contains_location(feature, location, len(query)):
            feature_location = feature["GBFeature_location"]
            protein_id = get_protein_id(feature["GBFeature_quals"])
            break

    return GenomeMatch(location, feature_location, protein_id)
