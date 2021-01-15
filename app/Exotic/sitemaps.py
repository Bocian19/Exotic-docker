from django.contrib.sitemaps import Sitemap
from carparts.models import Product
from django.urls import reverse


class TodoSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Product.objects.all()


class StaticViewSitemap(Sitemap):

    def items(self):
        return ['main-page', 'products', 'contact', 'about', 'bodykits']

    def location(self, item):
        return reverse(item)
