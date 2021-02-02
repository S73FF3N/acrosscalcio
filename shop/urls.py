from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.ProductListView.as_view(), name='product_list'),
    url(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.product_detail, name='product_detail'),
]