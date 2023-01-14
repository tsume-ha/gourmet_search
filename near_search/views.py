from django.views.generic import TemplateView

class TopPageView(TemplateView):
    template_name = "near_search/index.html"
    