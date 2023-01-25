from django.views.generic import TemplateView, ListView
from django.core.exceptions import SuspiciousOperation
from .forms import ShopSearchForm
from .hotpepper_api import API

class TopPageView(TemplateView):
    template_name = "near_search/index.html"
    
class ShopListView(ListView):
    template_name = "near_search/shop_list.html"
    allow_empty = True
    model = None
    paginate_by = 10
    total_shop_num = None
    shop_num = None
    shop_start_num = None

    def get_queryset(self):
        form = ShopSearchForm(self.request.GET)
        if not form.is_valid():
            raise SuspiciousOperation("invalid form request")
        # page 設定
        page_kwarg = self.page_kwarg
        page = self.kwargs.get(page_kwarg) or self.request.GET.get(page_kwarg) or 1
        shop_start_num = 1 + (int(float(page)) - 1) * 10 if int(float(page)) > 0 else 1

        hotpepper = API()
        data = hotpepper.getShopList(form.cleaned_data, shop_start_num=shop_start_num)
        self.total_shop_num = data["total_shop_num"]
        self.shop_num = data["shop_num"]
        self.shop_start_num = data["shop_start_num"]
        return data["shops"]

    def get_paginator(
            self, queryset, per_page, orphans=0, allow_empty_first_page=True, **kwargs
        ):
        all_list = list(range(self.total_shop_num))
        for i, shop in zip(range(self.shop_start_num - 1, self.shop_start_num + self.shop_num - 1), self.object_list):
            all_list[i] = shop
        # print(all_list)
        return self.paginator_class(
            all_list,
            per_page,
            orphans=orphans,
            allow_empty_first_page=allow_empty_first_page,
            **kwargs,
        )