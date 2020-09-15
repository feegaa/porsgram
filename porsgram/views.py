from django.shortcuts import render
from django.template import RequestContext
from porsgram.path import PAGE_404, PAGE_500, PAGE_400, PAGE_403

def handler404(request, *args, **argv):
    response = render(RequestContext(request), PAGE_404, {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(RequestContext(request), PAGE_500, {})
    response.status_code = 500
    return response



def handler400(request, *args, **argv):
    response = render(RequestContext(request), PAGE_400, {})
    response.status_code = 400
    return response



def handler403(request, *args, **argv):
    response = render(RequestContext(request), PAGE_403, {})
    response.status_code = 403
    return response