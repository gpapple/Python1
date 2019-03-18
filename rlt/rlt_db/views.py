from django.shortcuts import render

# Create your views here.
def one(request):
    c = dict()
    c['score'] = [10,20,30]
    return render(request,'one.html',context= c )

def two(request):
    c = dict()
    # c['name'] = '廖穗'
    c['name'] = '爱情'
    # c['name'] = '情'
    return render(request,'two.html',context= c)
