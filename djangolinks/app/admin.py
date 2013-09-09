# -*- coding: utf-8 -*-
"""Admin for emencia.django.links"""
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Link


class LinkAdmin(admin.ModelAdmin):
    #list_display = ('id','title', 'url', 'visibility','slug','featured','spotlight','publication_start', 'publication_end','logo','editor_rating','free','free_trial','one_month_price','two_month_price','three_month_price')
    #list_editable = ('title', 'url', 'visibility','featured','spotlight','publication_start', 'publication_end','logo','editor_rating','free','free_trial','one_month_price','two_month_price','three_month_price')
    #list_display_links = ('id',)
    date_hierarchy = 'creation'
    list_filter = ('visibility','creation')
    search_fields = ('title', 'description', 'url','tags')
    fieldsets = ((None, {'fields': ('owner','title','slug','description', 'url','logo','editor_rating','free','free_trial','one_month_price','two_month_price','three_month_price')}),
                 (_('Attributes'), {'fields': ('tags',)}),
                 (_('Metadata'), {'fields': ('visibility','publication_start', 'publication_end')}),
                 )
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Link, LinkAdmin)
