# グルメサーチ

## Install

### Djangoの起動

```
python -m venv venv
(activate)
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Tailwindの起動

```
python manage.py tailwind start
```
にて開発環境が構築される

### Tailwindのビルド

```
python manage.py tailwind build
```
にて圧縮されたCSSなどがビルドされる

### 環境変数

`.env`ファイルを`manage.py`と同じ階層に用意し、中身は
```
SECRET_KEY=
HOTPEPPER_API_KEY=
```
を用意する。

ホットペッパーグルメのAPIキー取得は
[ホットペッパー | ご利用案内](https://webservice.recruit.co.jp/doc/hotpepper/guideline.html)
より。
