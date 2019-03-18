from django.conf.urls import include, url
from django.contrib import admin
from rlt_db import views as f

urlpatterns = [
    # Examples:
    # url(r'^$', 'rlt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^one/',f.one),
    url(r'^two/',f.two)
]

