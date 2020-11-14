from django.http import JsonResponse
from api.protein import search_protein
from api.models import SearchResult


def start_search(request):
    query = request.GET["seq"]
    user_id = request.session["user_id"]
    protein = "NC_007346"
    match = search_protein(protein, query)
    if match is None:
        SearchResult.objects.create(user_id=user_id, query=query)
    else:
        SearchResult.objects.create(
            user_id=user_id,
            query=query,
            protein=protein,
            location=match.location,
            feature_location=match.feature_location,
            protein_id=match.protein_id,
        )
    return JsonResponse({"success": True})


def search_results(request):
    user_id = request.session["user_id"]
    results = [result.json() for result in SearchResult.objects.filter(user_id=user_id)]
    print(results)
    return JsonResponse({"success": True, "results": results})
