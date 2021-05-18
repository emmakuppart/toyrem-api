import requests

from django.conf import settings


def get_shop_config():
    response = requests.get(settings.PAYMENT_CENTER_API_URL + '/shop/configuration')
