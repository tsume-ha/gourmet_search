from django.urls import path
from .views import TopPageView, ShopListView

app_name = "near_search"

urlpatterns = [
    path("", TopPageView.as_view(), name="index"),
    path("search", ShopListView.as_view(), name="search")
]
