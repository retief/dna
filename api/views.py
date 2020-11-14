import json
import threading

from django.http import JsonResponse
from api.genome import search_genome
from api.models import SearchResult


def run_search(genome, query, result_id):
    match = search_genome(genome, query)
    if match is not None:
        defaults = {
            "genome": genome,
            "location": match.location,
            "feature_location": match.feature_location,
            "protein_id": match.protein_id,
        }
        SearchResult.objects.update_or_create(
            id=result_id,
            defaults=defaults,
        )


def start_search(request):
    query = json.loads(request.body)["query"]
    user_id = request.session["user_id"]
    genome = "NC_007346"
    result = SearchResult.objects.create(user_id=user_id, query=query)
    threading.Thread(target=run_search, args=(genome, query, result.id)).start()
    return JsonResponse({"success": True})


def search_results(request):
    user_id = request.session["user_id"]
    results = [result.json() for result in SearchResult.objects.filter(user_id=user_id)]
    return JsonResponse({"success": True, "results": results})
