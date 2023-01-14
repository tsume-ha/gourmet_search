from django.urls import path
from .views import TopPageView

urlpatterns = [
    path("", TopPageView.as_view()),
]
