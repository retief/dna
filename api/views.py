import json

from django.http import JsonResponse

from api.models import SearchResult
from api.tasks import run_search


def start_search(request):
    query = json.loads(request.body)["query"]
    user_id = request.session["user_id"]
    result = SearchResult.objects.create(user_id=user_id, query=query)
    run_search.delay(query, result.id, 0)
    return JsonResponse({"success": True})


def search_results(request):
    user_id = request.session["user_id"]
    results = [result.json() for result in SearchResult.objects.filter(user_id=user_id)]
    return JsonResponse({"success": True, "results": results})
