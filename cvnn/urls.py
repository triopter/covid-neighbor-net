"""cvnn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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

from engagements import views as engagement_views
from neighbors import views as neighbor_views

urlpatterns = [
    path(
        'engagements/created/<int:engagement_id>/',
        engagement_views.create_engagement_thanks,
        name='create_engagement_thanks',
    ),
    path('engagements/create/', engagement_views.create_engagement, name='create_engagement'),
    path(
        'engagements/<int:engagement_id>/claim/',
        engagement_views.claim_engagement,
        name='claim_engagement',
    ),
    path(
        'engagements/<int:engagement_id>/',
        engagement_views.engagement_detail,
        name='engagement_detail',
    ),
    path('engagements/', engagement_views.search_engagements, name='search_engagements'),
    path(
        'register/requester/',
        engagement_views.register_and_create_engagement,
        name='register_and_create_engagement',
    ),
    path(
        'register/volunteer/<int:engagement_id>/',
        engagement_views.register_and_claim_engagement,
        name='register_and_claim_engagement',
    ),
    path('', neighbor_views.home, name='home'),
    path('admin/', admin.site.urls),
]
