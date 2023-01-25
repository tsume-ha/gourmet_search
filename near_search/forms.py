from django import forms
from django.db import models

class RangeChoices(models.IntegerChoices):
    """
    緯度経度から検索するときの範囲の半径の大きさ
    """
    R300m = 1
    R500m = 2
    R1000m = 3
    R2000m = 4
    R3000m = 5

class ShopSearchForm(forms.Form):
    # フィールドの名前はそのままAPIに流すので、APIのキーと同じにしておく
    lat = forms.FloatField(initial=35.669220, help_text="緯度")
    lng = forms.FloatField(initial=139.761457, help_text="経度")
    range = forms.ChoiceField(choices=RangeChoices.choices, initial=RangeChoices.R1000m, required=False)
    keyword	 = forms.CharField(max_length=256, required=False)
