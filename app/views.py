from django.http import HttpResponse


def health_check(_):

    return HttpResponse(status=200)
