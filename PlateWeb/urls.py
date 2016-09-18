"""PlateWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,patterns, include
from django.contrib import admin
from Plate import views

extra_patterns = patterns('',  
    
    url(r'^label/',views.index,name='index'),
    url(r'^nextPage/',views.nextPage,name='nextPage'),
    url(r'^delPlate/',views.delPlate,name='delPlate'),
    url(r'^getRestImgCountOnLoad/',views.getRestImgCountOnLoad,name='getRestImgCountOnLoad'),

    url(r'',views.index,name='index'),
) 

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #url(r'^car/',views.index,name='index'),
    url(r'^car/',include(extra_patterns)),
    url(r'^car_sub/',views.sub,name='car_sub'),
    url(r'^manage/',views.manage,name='manage'),
]



