from django.contrib.sitemaps import Sitemap
from .models import PostModel


class PostSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9

    def items(self):
        return PostModel.published.all()

    def lastmod(self, obj):
        return obj.updated