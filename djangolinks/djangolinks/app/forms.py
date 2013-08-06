from django.forms import ModelForm

from models import Link
from django import forms
from django.utils.translation import ugettext as _

from haystack.query import SearchQuerySet
import logging

# Create the form class.
class LinkSubmitForm(ModelForm):
    owner_email = forms.EmailField(help_text='We will use this email for matching your social account')
    owner_username = forms.RegexField(max_length=30, regex=r'^\w+$',help_text='This username will shown as in link submitted by')

    class Meta:
        model = Link
        exclude=('total_votes','owner','slug','publication_start','publication_end','visibility','featured','spotlight',
                 'logo','editor_rating','free','free_trial','one_month_price','two_month_price','three_month_price'
                 )


from haystack.forms import SearchForm

class LinkSearchForm(SearchForm):
    tags = forms.CharField(required=False)
 
    def search(self):
        sqs = self.searchqueryset.all()
 
        if not self.is_valid():
            return sqs
 
        if self.cleaned_data['q']:
            sqs = sqs.auto_query(self.cleaned_data['q'])
 
        if self.cleaned_data['tags']:
            sqs = sqs.filter(tags__in=self.cleaned_data['tags'].split())
 
        if self.load_all:
            sqs = sqs.load_all()

        return sqs
    

class LinkSearchForm2(SearchForm):
    def __init__(self, *args, **kwargs):
        super(LinkSearchForm2, self).__init__(*args, **kwargs)
        self.fields['tags'] = forms.CharField(required=False)
        self.fields['free'] = forms.CharField(required=False)

    def get_tags(self):
        search_tags = []
        
        if self.is_valid():
            for tag in self.cleaned_data['tags'].split():
                search_tags.append(tag)
        
        return search_tags

    def search(self):
              
        if not self.is_valid():
            return self.no_query_found()
        else:
            if self.cleaned_data['free'] and not self.cleaned_data['free']=='All':
                return self.searchqueryset.filter(content=self.cleaned_data['q']).filter(tags__in=self.get_tags()).filter(free=self.cleaned_data['free'])
            else:
                return self.searchqueryset.filter(content=self.cleaned_data['q']).filter(tags__in=self.get_tags())
            
             
        

    def no_query_found(self):
        return self.searchqueryset.all()
