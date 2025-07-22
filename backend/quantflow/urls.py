"""
URL configuration for quantflow project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from backtestapi import views
from blog.views import ArticleListCreateView, ArticleDetailView, CategoryListView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/fixedstrategy/", views.fixed_strategy),
    path("api/available_indicators/", views.available_indicators),
    path("api/indicator_schema/", views.indicator_schema),
    path("api/customstrategy/", views.custom_strategy),
    path('api/blog/', ArticleListCreateView.as_view(), name='article-list'),
    path('api/blog/<int:pk>/', ArticleDetailView.as_view()),
    path('api/categories/', CategoryListView.as_view(), name='category-list'),
    path('api/symbols/', views.list_symbols),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)