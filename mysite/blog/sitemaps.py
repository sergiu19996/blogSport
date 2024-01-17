from django.contrib.sitemaps import Sitemap
from .models import Post

class PostSitemap(Sitemap):
    changefreq = 'weekly'
    prioority = 0.9

def items(self):
    def lasmod(self, obj)
        return obj.updated