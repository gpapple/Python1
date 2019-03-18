from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def do_normalmap(request):
    return HttpResponse('倘若他日相见，我将何以贺你，以眼泪，以沉默')
def withparam(r,year,month):
    return HttpResponse("Year is:{0},Month is:{1}".format(year,month))
def do_app(request):
    return HttpResponse('这是一个子路由')
def do_page(request,pn):
    return HttpResponse('Your page is {0}'.format(pn))
def revparse(request):
    return HttpResponse('Your request URL is {0}'.format(reverse("askname")))