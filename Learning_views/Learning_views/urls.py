from django.conf.urls import include, url
from django.contrib import admin
from do_views import views as f
urlpatterns = [
    # Examples:
    # url(r'^$', 'Learning_views.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^v1/',f.v1),
    url(r'^v2/',f.v2,),
    url(r'^v3/',f.v3,name="nice"),

    url(r'v4_get/',f.v4_get),
    url(r'v4_post/',f.v4_post),
    # url(r'^render_test/',f.render_test),
    # url(r'^render_test1/',f.render_test1),
    url(r'^render_test2/',f.render_test2),
    url(r'^Http1/(?:page-(?P<pages>\d+))$',f.http,name="http"),
    url(r'^v3_get/',f.v3_get),
]
