from django.conf.urls import url
from . import views
from rest_framework.routers import DefaultRouter

routes = DefaultRouter()
# routes.register(r'node',views.NodeDumpDetial)
urlpatterns = [

    url(r'^nodes/$',views.NodeDumpList.as_view()),
    url(r'^nodes/(?P<pk>\d+)$',views.NodeDumpDetial.as_view()),
    url(r'^gencode/(?P<pk>\d+)$',views.GencodeDetial.as_view()),
    url(r'^name/(?P<pk>\d+)$',views.NameDetial.as_view()),
    url(r'^citations/(?P<pk>\d+)$',views.CitationsDetial.as_view()),
    url(r'^division/(?P<pk>\d+)$',views.DivisionDetial.as_view()),
    # url(r'^/$',views.NodeDumpDetial.as_view()),


]

urlpatterns += routes.urls
