from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^', include('allstar_teams.urls')),
    path(r'^shop/', include(('shop.urls', 'shop'), namespace='shop')),
    path(r'^cart/', include(('cart.urls', 'cart'), namespace='cart')),
    path(r'^order/', include(('order.urls', 'order'), namespace='order')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
