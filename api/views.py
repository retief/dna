from django.http import HttpResponse
from Bio import Entrez

def index(request):
    query = request.GET["seq"]

    protein = "NC_007346"
    with Entrez.efetch(db="nuccore", id=protein, rettype="gb", retmode="xml") as handle:
        record = Entrez.read(handle)
    seq = record[0]["GBSeq_sequence"]

    loc = seq.find(query)
    if loc == -1:
        return HttpResponse("Sequence not found")

    features = record[0]["GBSeq_feature-table"]
    for feature in features:
        if feature["GBFeature_key"] != "CDS":
            continue

        interval = feature["GBFeature_intervals"][0]
        start = int(interval["GBInterval_from"])
        end = int(interval["GBInterval_to"])
        # when the location is a complement, start > end so use min and max to ensure I'm checking
        # whether the sequence is in the range correctly
        lower = min(start, end)
        upper = max(start, end)
        if loc > upper or loc + len(query) < lower:
            continue

        location = feature["GBFeature_location"]
        protein_id = "No ID"
        for qual in feature["GBFeature_quals"]:
            if qual["GBQualifier_name"] == "protein_id":
                protein_id = qual["GBQualifier_value"]
                break
        return HttpResponse(f"Found sequence, protein: {protein}, loc: {loc}, feature_range: {location}, protein_id: {protein_id}")

    return HttpResponse(f"Found sequence, protein: {protein}, loc: {loc}")
