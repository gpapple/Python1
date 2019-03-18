from django.shortcuts import render,render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator
def v1(r):
    return HttpResponse('v3')

def v2(r):
    return HttpResponseRedirect('v3')
def v3(r):
    return HttpResponse('这是你要访问的地址{0}'.format(reverse("nice")))
def v3_get(r):
    rst = '...'
    k= r.GET.getlist('name')

    # rst+= k + '-->'+ v
    rst+=','
    return HttpResponse(k)
def v4_get(r):
    return render_to_response('for-post.html')
def v4_post(r):
    rst = '...'
    for k,v in r.POST.items():
        rst += k + '-->' + v
        rst +=','
    return HttpResponse('Get value of post is {0}'.format(rst))

def render_test(req):
    rsp = render(req,'render.html')
    return rsp

def render_test1(req):
    x = dict()
    x['name2'] = 'kob'
    x['name2'] = 'kob one'
    x['name2'] = 'kdkg'
    rsp = render(req,'render.html',context=x)
    return rsp

def render_test2(req):
    from django.template import loader
    t = loader.get_template('render.html')
    print(type(t))
    rsp = t.render({'name':"superman"})
    print(type(rsp))
    return HttpResponse(rsp)
def http(request,pages):
    return HttpResponse ('The page is {0}'.format(pages))

# Create your views here.
