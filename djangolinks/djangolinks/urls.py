from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()


from django.conf.urls.defaults import *

from django.views.generic import ListView,DetailView,TemplateView

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

from app.models import Link
from app.forms import LinkSubmitForm
from app.views import IndexView,LinkCreateView,SearchView,LinkDetailView,FavoriteListView


from haystack.forms import ModelSearchForm
from haystack.query import SearchQuerySet
from haystack.views import SearchView, search_view_factory
from app.forms import LinkSearchForm2


from tagging.views import tagged_object_list

from django.contrib.auth import logout as auth_logout

from app.models import Link,Favorite

from django.contrib.auth.decorators import login_required
from hitcount.views import update_hit_count_ajax

from dajaxice.core import dajaxice_autodiscover 
dajaxice_autodiscover()

from app.feeds import RssLatestLinksFeed

from app.views import LinkListView,SearchView2,tagged_links


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangolinks.views.home', name='home'),
    # url(r'^djangolinks/', include('djangolinks.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),

     url(r'^$', IndexView.as_view(),name="index"),
     url(r'^list/$', LinkListView.as_view(paginate_by=settings.RESULTS_PER_PAGE),name="list"),
     url(r'^favorite/$', login_required(FavoriteListView.as_view(paginate_by=settings.RESULTS_PER_PAGE)),name="favorite"),
     url(r'^detail/([-\w]+)-(?P<pk>\d+)/$',LinkDetailView.as_view(model=Link),name="detail"),
     url(r'^submit/$',LinkCreateView.as_view(model=Link,form_class=LinkSubmitForm,template_name='app/link_submit.html'),name="submit"),

     url(r'^search/$', search_view_factory(
        view_class=SearchView2,
        template='app/link_list.html',
        form_class=LinkSearchForm2,
    ), name='haystack_search'),
 
     url(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),
     url(r'^contact/', include('contact_form.urls',namespace='contact_form',app_name='contact_form')),
     url(r'', include('social_auth.urls')),
     url(r'^login/$', TemplateView.as_view(template_name="app/login.html"),name="login"),
     url(r'^about/$', TemplateView.as_view(template_name="app/about.html"),name="about"),
     url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),
     url(r'^register/$', TemplateView.as_view(template_name="app/register.html"),name="register"),
     url(r'^login-error/$', TemplateView.as_view(template_name="app/login_failure.html"),name="login-error"),

     url(r'^feed/rss/latest/$', RssLatestLinksFeed()),
     url(r'^comments/', include('django.contrib.comments.urls')),

     url(r'^tag/(?P<tag>[^/]+)/$',tagged_links,name='tag'),
     url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'document_root': settings.STATIC_ROOT,
     }),
                       
     url(r'^ajax/hit/$', # you can change this url if you would like
        update_hit_count_ajax,
        name='hitcount_update_ajax'), # keep this name the same


)


urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'document_root': settings.STATIC_ROOT,
        }),
   )

