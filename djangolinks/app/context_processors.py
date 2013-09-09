from django.contrib.sites.models import Site
from models import Link

def spotlight(request):
    return {
        'spotlight': Link.published.filter(spotlight=True).order_by('?')[0] if Link.published.filter(spotlight=True) else None
        }




def site_domain(request):
    current_site = Site.objects.get_current()
    return {
        'site_domain': current_site.domain
        }

def site_name(request):
    current_site = Site.objects.get_current()
    return {
        'site_name': current_site.name
        }
    

from django.conf import settings # import the settings file

def site_twitter_id(context):
    # return the value you want as a dictionnary. you may add multiple values in there.
    return {'site_twitter_id': settings.SITE_TWITTER_ID}    