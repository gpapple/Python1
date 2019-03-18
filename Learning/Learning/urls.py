from django.conf.urls import include, url
from django.contrib import admin
from teacher import views as f
from teacher import teacher_url

urlpatterns = [
    # Examples:
    # url(r'^$', 'Learning.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    # url(r'^normalmap/',f.do_normalmap)
    url(r'^withparam/(?P<year>[0-9]{4})/(?P<month>[0,1][0-9])',f.withparam),
    url(r'^teacher/',include('teacher.teacher_url')),
    url(r'^book/(?:page-(?P<pn>\d+))$',f.do_page),
    url(r'^rname/',f.revparse, name="askname")
    ]

