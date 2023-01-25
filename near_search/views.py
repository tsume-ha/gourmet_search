from django.views.generic import TemplateView, ListView
from django.core.exceptions import SuspiciousOperation
from .forms import ShopSearchForm
from .hotpepper_api import Shop, API

class TopPageView(TemplateView):
    template_name = "near_search/index.html"
    
class ShopListView(ListView):
    template_name = "near_search/shop_list.html"
    allow_empty = True
    model = None

    def get_queryset(self):
        form = ShopSearchForm(self.request.GET)
        if not form.is_valid():
            raise SuspiciousOperation("invalid form request")
        hotpepper = API()
        return hotpepper.getShopList(form.cleaned_data)