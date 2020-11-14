from django.http import HttpResponse
from api.protein import search_protein
from api.models import SearchResult


def start_search(request):
    query = request.GET["seq"]
    user_id = request.session["user_id"]
    protein = "NC_007346"
    match = search_protein(protein, query)
    if match is None:
        SearchResult.objects.create(user_id=user_id)
    else:
        SearchResult.objects.create(
            user_id=user_id,
            protein=protein,
            location=match.location,
            feature_location=match.feature_location,
            protein_id=match.protein_id,
        )
    return HttpResponse("Started search")
