# Create your views here.

from django.conf import settings
from models import Favorite,Vote,Link
from django.views.generic import TemplateView,ListView,CreateView
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from haystack.views import SearchView
from django import forms
from tagging.views import tagged_object_list
from twitter import Twitter,NoAuth,OAuth,read_token_file
import os
from django.core.mail import send_mail
from django.contrib.sites.models import Site

class IndexView(TemplateView):
    template_name = "app/index.html"
   
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['featured_links'] = Link.published.filter(featured=True)[:5]
        context['latest_links'] = Link.published.filter()[:5]
        #context['random_links'] = Link.published.filter(favorite__id__in=Favourite.objects.filter(owner=self.request.user)).order_by('-creation')[:5]
        context['random_links'] = Link.published.order_by('?')[:5]
           
        return context

from django.views.generic import DetailView

class LinkDetailView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(LinkDetailView, self).get_context_data(**kwargs)
        context['is_favorite_link_of_user'] = Favorite.objects.filter(link=self.kwargs['pk'],owner=self.request.user.id).exists()
        context['is_up_voted_link_of_user'] = Vote.objects.filter(link=self.kwargs['pk'],owner=self.request.user.id,direction=1).exists()
        context['is_down_voted_link_of_user'] = Vote.objects.filter(link=self.kwargs['pk'],owner=self.request.user.id,direction=-1).exists()
        return context

class LinkCreateView(CreateView):

    def get_form(self, form_class):
        form = super(LinkCreateView,self).get_form(form_class)
        if  self.request.user.is_authenticated():
            #form.fields['owner_email'].required=False
            #form.fields['owner_username'].required=False
            del form.fields["owner_email"]
            del form.fields["owner_username"]
        else:
            try:
              form.fields['owner_email'].initial=self.request.session['owner_email']
              form.fields['owner_username'].initial=self.request.session['owner_username']
            except KeyError:
              pass
               
        return form

    def form_valid(self, form):
        link = form.save(commit=False)
        

        is_authenticated=self.request.user.is_authenticated()

        if not is_authenticated: 
           owner ,created = User.objects.get_or_create(email=form.cleaned_data['owner_email'],defaults={'username':form.cleaned_data['owner_username']})
           try:
              self.request.session['owner_email'] = form.cleaned_data['owner_email']
              self.request.session['owner_username'] = form.cleaned_data['owner_username']
           except KeyError:
              pass

           if created:
              owner.save()
        else:
           owner=self.request.user
        
        link.owner=owner
        link.save()

        T_PATH = os.path.join(settings.ROOT_PATH,'twitter')
        oauth = OAuth(*read_token_file('%s/oauth_creds' % T_PATH)
               + ('%s' % settings.TWITTER_CONSUMER_KEY,'%s' % settings.TWITTER_CONSUMER_SECRET))

        twitter = Twitter(domain='api.twitter.com',
                  auth=oauth,
                  api_version='1')

        link_detail_url='%s/detail/%s-%s %s' % (Site.objects.get_current().domain,link.slug,link.id,link.title)


        twitter.statuses.update(status='%s' % link_detail_url)

        if settings.INFORM_NEW_LINKS:
            
            send_mail('%s' % Site.objects.get_current().name,'%s' % link_detail_url, 'mailer@%s' % Site.objects.get_current().domain ,[settings.ADMINS[0][1]], fail_silently=True)
     
          
        return HttpResponseRedirect(link.get_absolute_url())
        #return HttpResponseRedirect('http://%s/detail/%s-%s' % (Site.objects.get_current().domain,link.slug,link.id))



class FavoriteListView(ListView):
    context_object_name = "link"
    def get_queryset(self):
        return Link.published.filter(favorite__id__in=Favorite.objects.filter(owner=self.request.user)).order_by('-creation')


sort_by = {
    'd': '-creation',
    't': 'title',
    'v': '-total_votes',
}

class LinkListView(ListView):
    context_object_name = "link"
    def get_queryset(self):
        sort = self.request.GET.get('sort')
        if sort in sort_by.keys():
           return Link.published.filter().order_by('%s' % sort_by[sort])
        else:
           return Link.published.filter().order_by('-creation')

class SearchView2(SearchView):
    def get_results(self):
        results = super(SearchView2, self).get_results() 
        sort = self.request.GET.get('sort')

        if sort in sort_by.keys():
           return results.order_by('%s' % sort_by[sort])
        else:
           return results.order_by('-creation')



from tagging.views import tagged_object_list

def tagged_links(request,tag):

    sort = request.GET.get('sort')
    queryset=None
    
    if sort in sort_by.keys():
       queryset=Link.published.filter().order_by('%s' % sort_by[sort])
    else:
       queryset=Link.published.filter().order_by('-total_votes')

    
    return tagged_object_list(request,queryset,tag,paginate_by=settings.RESULTS_PER_PAGE,allow_empty=True, template_object_name="object_list")
