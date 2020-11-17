import uuid


def user_id_middleware(get_response):
    """Add a user_id to the session if the session doesn't already have a user_id

    We don't need proper user accounts or anything, so this is all the auth we need.
    I added this as middleware because I didn't want to have to copy/paste this code
    (or a call to a function that did this) into every view.
    """

    def middleware(request):
        request.session.setdefault("user_id", str(uuid.uuid1()))
        return get_response(request)

    return middleware
