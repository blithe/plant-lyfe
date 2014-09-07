from django.conf.urls import patterns, include, url

from plant_lyfe_app.models import Plant, Leaf
from plant_lyfe_app.views import PlantList, PlantDetail, LeafDetail
from plant_lyfe_app.serializers import PlantListSerializer, PlantSerializer, LeafSerializer


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plant_lyfe_site.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^dicots/$', PlantList.as_view()),
    url(r'^dicots/(?P<slug>[\w-]+)/$', PlantDetail.as_view()),
    url(r'^dicots/(?P<plant_slug>[\w-]+)/leaf/(?P<pk>\d+)/$', LeafDetail.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^admin/', include(admin.site.urls)),
)
