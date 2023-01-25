import urllib.parse
from django.views.generic import TemplateView, ListView, DetailView
from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from .forms import ShopSearchForm
from .models import Shop
from .hotpepper_api import API

class TopPageView(TemplateView):
    template_name = "near_search/index.html"
    
class ShopListView(ListView):
    template_name = "near_search/shop_list.html"
    allow_empty = True
    model = None
    search_queries = None
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
        self.search_queries = form.cleaned_data
        data = hotpepper.getShopList(self.search_queries, shop_start_num=shop_start_num)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # ページ位置情報を保存しておく
        paginator_urls = {
            "first": "/search?" + urllib.parse.urlencode({**self.search_queries, **{"page": 1}}),
            "prev": "/search?" + urllib.parse.urlencode({**self.search_queries, **{"page": context["page_obj"].previous_page_number() if context["page_obj"].has_previous() else 1 }}),
            "current": "/search?" + urllib.parse.urlencode(self.search_queries),
            "next": "/search?" + urllib.parse.urlencode({**self.search_queries, **{"page": context["page_obj"].next_page_number() if context["page_obj"].has_next() else context["page_obj"].paginator.num_pages}}),
            "last": "/search?" + urllib.parse.urlencode({**self.search_queries, **{"page": context["page_obj"].paginator.num_pages}})
        }
        context["paginator_urls"] = paginator_urls
        return context


class ShopView(DetailView):
    template_name = "near_search/shop.html"
    model = Shop

    def get_object(self, queryset=None):
        try:
            return super().get_object(queryset)
        except Http404:
            print("直接個別ページにアクセスしたため、APIから取得し直します。")
            hotpepper = API()
            shop = hotpepper.getShopById(self.kwargs.get(self.pk_url_kwarg))
            if shop is None:
                raise Http404()
            return shop
