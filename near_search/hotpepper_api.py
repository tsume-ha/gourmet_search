import requests
import xml.etree.ElementTree as ET
from django.conf import settings

class Shop:
    id: str = ""
    name: str = ""
    photo_url: str = ""
    address: str = ""
    open: str = ""
    close: str = ""
    catch: str = ""
    access: str = ""
    genre_name: str = ""
    genre_catch: str = ""

    def __str__(self) -> str:
        return f"{self.name} (id: {self.id})"


class API:
    API_KEY = settings.HOTPEPPER_API_KEY
    ns = {# name space
        "hp": "http://webservice.recruit.co.jp/HotPepper/"
    }

    def _shop_parse(self, elem:ET.Element):
        s = Shop()
        s.id = elem.find("hp:id", self.ns).text
        s.name = elem.find("hp:name", self.ns).text
        s.address = elem.find("hp:address", self.ns).text
        s.open = elem.find("hp:open", self.ns).text
        s.close = elem.find("hp:close", self.ns).text
        s.catch = elem.find("hp:catch", self.ns).text
        s.access = elem.find("hp:access", self.ns).text
        s.genre_name = elem.find("hp:genre", self.ns).find("hp:name", self.ns).text
        s.genre_catch = elem.find("hp:genre", self.ns).find("hp:catch", self.ns).text
        s.photo_url = elem.find("hp:photo", self.ns).find("hp:pc", self.ns).find("hp:l", self.ns).text
        print(s)
        return s


    def getShopList(self, params, shop_start_num=1):
        URL = "http://webservice.recruit.co.jp/hotpepper/gourmet/v1/"
        print(params)
        print("API calling start")
        res = requests.get(
            url=URL,
            params={**params, **{"key": self.API_KEY, "start": shop_start_num}}
        )
        print("API calling end")
        res_tree = ET.fromstring(res.text)

        # APIバージョンの確認
        if res_tree.find("hp:api_version", self.ns).text != "1.26":
            print("HotpepperのAPIバージョンが異なるため、正しく解析できていない可能性があります")
        
        # ページネーション関連
        total_shop_num = res_tree.find("hp:results_available", self.ns).text
        # 検索結果総数
        shop_num = res_tree.find("hp:results_returned", self.ns).text
        # このリクエストでの表示件数
        shop_start_num = res_tree.find("hp:results_start", self.ns).text
        # このリクエストでの開始番号
        print(total_shop_num, shop_num, shop_start_num)
        
        shops = [self._shop_parse(shop_elem) for shop_elem in res_tree.findall("hp:shop", self.ns)]
    
        return {
            "shops": shops,
            "total_shop_num": int(total_shop_num),
            "shop_num": int(shop_num),
            "shop_start_num": int(shop_start_num)
            }