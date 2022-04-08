from django.http import HttpResponse
from django.http import HttpResponseRedirect


def health_check(_) -> HttpResponse:

    return HttpResponse(status=200)


def index(_) -> HttpResponseRedirect:

    return HttpResponseRedirect("/admin/")
