from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _

from blog.models import Article

class LatestEntriesFeed(Feed):
    title = "Blog"
    #link = "/feed/"

    def items(self):
        return Article.objects.get_published_live()[:10]

    def item_title(self, item):
        return item.translated.title

    def item_description(self, item):
        return item.translated.content

    # item_link is only needed if NewsItem has no get_absolute_url method.
    # def item_link(self, item):
    #     return item.get_absolute_url()