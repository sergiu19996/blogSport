import markdown
from django.contrib.syndication.views import feed 
from django.template.defaultfilters import truncatewords_html
from django.urls import reverse_lazy
from .models import Post 


class LatestPostsFeed(Feed):
    title = 'My blog'
    link = reverse_lazy('blog:post_list')
    description = 'new posts of my blog.'

    def iteams(self)
        return Post.published.all()[:5]
    
    def iteam_title(self, iteam):
        return iteam.title
     
    def iteam_description(self, iteam):
        return truncatewords_html(markdown.markdown(iteam.body),30)
    
    def iteam_pubdatte(self, iteam):
        return iteam.publish