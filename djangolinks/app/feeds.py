from django.contrib.syndication.views import Feed
from models import Link
from django.utils.feedgenerator import Atom1Feed
from django.utils.text import truncate_words
from django.contrib.sites.models import Site

class RssLatestLinksFeed(Feed):
    feed_type = Atom1Feed

    title = "%s Latest Links" % Site.objects.get_current().domain
    description = "Latest links in %s " % Site.objects.get_current().domain
    subtitle = description
    link="/"

    def items(self):
        return Link.published.filter().order_by('-creation')[:15]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return truncate_words(item.description,20)
