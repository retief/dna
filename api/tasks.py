import random

from celery import shared_task

from api.genome import search_genome
from api.models import SearchResult

GENOMES = [
    "NC_000852",
    "NC_007346",
    "NC_008724",
    "NC_009899",
    "NC_014637",
    "NC_020104",
    "NC_023423",
    "NC_023640",
    "NC_023719",
    "NC_027867",
]


@shared_task
def run_search(query, result_id, call_count):
    if call_count > 40:
        # we probably should stop the search eventually so that we don't have an
        # infinite loop on failing searches.  With 10 things to search, there's
        # about a 1.5% chance of not testing a given genome after 40 tries.  That
        # seems like enough certainty for now, though we'd probably want a different
        # condition here in a production version of this app.
        return
    genome = GENOMES[random.randrange(10)]
    match = search_genome(genome, query)
    if match is None:
        run_search.delay(query, result_id, call_count + 1)
    else:
        defaults = {
            "genome": genome,
            "location": match.location,
            "feature_location": match.feature_location or "",
            "protein_id": match.protein_id or "",
        }
        SearchResult.objects.update_or_create(
            id=result_id,
            defaults=defaults,
        )
