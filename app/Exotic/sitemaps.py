from django.contrib.sitemaps import Sitemap
from carparts.models import Product
from django.urls import reverse


class TodoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    protocol = 'htps'

    def items(self):
        return Product.objects.all()

    def lastmod(self, obj):
        return obj.pub_date


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['main-page', 'products', 'contact', 'about', 'bodykits']

    def location(self, item):
        return reverse(item)
