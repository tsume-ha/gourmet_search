from django.urls import path
from .views import TopPageView, ShopListView, ShopView

app_name = "near_search"

urlpatterns = [
    path("", TopPageView.as_view(), name="index"),
    path("search", ShopListView.as_view(), name="search"),
    path("shop/<str:pk>", ShopView.as_view(), name="shop")
]
