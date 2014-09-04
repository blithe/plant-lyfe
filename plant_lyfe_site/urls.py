from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import plant_lyfe_app.views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plant_lyfe_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', plant_lyfe_app.views.index, name='index'),
    url(r'^admin/', include(admin.site.urls)),
)
