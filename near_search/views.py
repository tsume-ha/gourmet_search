from django.views.generic import TemplateView, ListView
from .hotpepper_api import Shop

class TopPageView(TemplateView):
    template_name = "near_search/index.html"
    
class ShopListView(ListView):
    template_name = "near_search/shop_list.html"
    allow_empty = True
    model = None

    def get_queryset(self):
        s1 = Shop()
        s1.name = "shop 1"
        s1.id = "s1"
        s1.logo_image = "url"
        s2 = Shop()
        s2.name = "shop 2"
        s2.id = "s2"
        s2.logo_image = "url"
        s3 = Shop()
        s3.name = "shop 3"
        s3.id = "s3"
        s3.logo_image = "url"
        return [s1, s2, s3]