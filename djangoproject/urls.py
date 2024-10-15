"""
URL configuration for djangoproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from myapp import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.Index),
    path("commodity/", views.Commodity),
    path("login/", views.Login.as_view()),
    path("logined/", views.logined),
    path("reg/", views.Reg.as_view()),
    path('Commodity/', views.Commodity_view),
    # path('jf_Commodity/', views.jf_Commodity_view),
    path('logout/', views.logout),
    path('discount/', views.discount),
    path('face/', views.face),
    path('exchange/', views.exchange),
    path('identity/', views.identity),
    path('favorite/', views.favorite_product, name='favorite_product'),
    path('favorite_list/', views.favorite_list, name='favorite_list'),
    path('favorites/remove/<int:product_id>/', views.remove_favorite, name='remove_favorite'),
    path('jf_Commodity/', views.jf_commodity_list, name='jf_commodity_list'),
    path('jf_commodity/exchange/<int:product_id>/', views.exchange_product, name='exchange_product'),
    path('addcart/', views.addcart),
    path('cart/', views.cart),
    path('check_login/',views.check_login),
    path('face_recognition_result/', views.face_recognition_result, name='face_recognition_result'),
    path('face/', views.face, name='face'),
    path('robot-camera-feed/', views.robot_camera_feed, name='robot_camera_feed'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
