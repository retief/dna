import uuid

def user_id_middleware(get_response):
    def middleware(request):
        request.session.setdefault("user_id", str(uuid.uuid1()))
        return get_response(request)

    return middleware
