# -*- coding: utf-8 -*-
from datetime import datetime

from django.db import models
from django.contrib.sites.models import Site
from django.utils.translation import ugettext as _
from django.conf import settings
from tagging.fields import TagField
#from tagging_autocomplete.models import TagAutocompleteField

from django.template.defaultfilters import slugify
from django.contrib.auth.models import User


RATINGS = (
    ('1', 'Poor'),
    ('2', 'Bad'),
    ('3', 'Average'),
    ('4', 'Good'),
    ('5', 'Excellent'),
)

YESNO = (
         ('Yes','Yes'),
         ('No','No')
         
         )

class LinkPublishedManager(models.Manager):
    """Link published manager"""

    def get_query_set(self):
        now = datetime.now()
        return super(LinkPublishedManager, self).get_query_set().filter(
            publication_start__lte=now, publication_end__gt=now,
            visibility=True).order_by('-creation')


    def favorites_for_user(self, user):
        """ Returns Favorites for a specific user
        """
        return self.get_query_set().filter(favorite__id__in=Favorite.objects.filter(owner=self.request.user)).order_by('-creation')


class Link(models.Model):
    """Link Model"""
    title = models.CharField(_('title'), max_length=150, default=None,unique=True)
    slug = models.SlugField(_('slug'), help_text=_('Used for the URLs'))
    url = models.URLField(_('url'), default=None,unique=True)
    description = models.TextField(_('description'))
    tags = TagField(null=False,blank=False)
    
    free = models.CharField(_('free'), choices=YESNO,default='No',max_length=3)
    free_trial = models.NullBooleanField(_('free trial'), default=None,null=True,blank=True)
    logo = models.CharField(_('logo'), max_length=255, default=None,null=True,blank=True)
    editor_rating=models.CharField(_('editor rating'),max_length=1, choices=RATINGS,null=True,blank=True)
    one_month_price = models.CharField(_('1 month price'), max_length=50, default=None,null=True,blank=True)
    two_month_price = models.CharField(_('2 month price'), max_length=50, default=None,null=True,blank=True)
    three_month_price = models.CharField(_('3 month price'), max_length=50, default=None,null=True,blank=True)

    visibility = models.BooleanField(_('visibility'), default=True)

    publication_start = models.DateTimeField(_('publication start'),default=datetime.now)
    publication_end = models.DateTimeField(_('publication end'),default=datetime(2042, 3, 15))

    featured = models.BooleanField(_('featured'), default=False,help_text=_('shown as highligted background in list'))
    spotlight = models.BooleanField(_('spotlight'), default=False,help_text=_('shown at spotlight section of djangolinks'))

    creation = models.DateTimeField(_('creation date'), auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True,auto_now_add=True,editable=False)
  
    total_votes = models.SmallIntegerField(default=0)

    objects = models.Manager()
    published = LinkPublishedManager()

    owner = models.ForeignKey(User,help_text=_('Your email address'))

    def save(self, *args, **kwargs):
        self.slug=slugify(self.title)
        super(Link, self).save(*args, **kwargs) # Call the "real" save() method.
        

    def get_absolute_url(self):
        return '/detail/%s-%s' % (self.slug,self.id)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')
        ordering = ('title',)
        

        


SCORES = (
    (u'+1', +1),
    (u'-1', -1),
)

class Favorite(models.Model):
    owner = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    creation = models.DateTimeField(_('creation date'), auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True,auto_now_add=True,editable=False)

class Vote(models.Model):
    owner = models.ForeignKey(User)
    link = models.ForeignKey(Link)
    direction = models.SmallIntegerField(choices=SCORES)
    creation = models.DateTimeField(_('creation date'), auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True,auto_now_add=True,editable=False)


    class Meta:
        unique_together = (('owner', 'link'),)
