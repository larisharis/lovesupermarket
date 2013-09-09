from django.utils import simplejson
from dajaxice.core import dajaxice_functions

import random
from dajax.core import Dajax
from dajaxice.decorators import dajaxice_register

from django.utils import simplejson
from dajaxice.core import dajaxice_functions

from dajaxice.decorators import dajaxice_register
from models import Favorite,Link,Vote

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

@dajaxice_register
def dajaxice_favorite(request,link):
    l=Link.objects.get(id=link)
    owner=User.objects.get(id=request.user.id)
    status=None
    f,c=Favorite.objects.get_or_create(owner=owner,link=l)
    if not c:
       f.delete()
       status="icon-star-empty" 
    else:
       f.save()
       status="icon-star" 
    return simplejson.dumps({'message':'%s' % status })

@dajaxice_register
def dajaxice_vote(request,link,direction):
    l=Link.objects.get(id=link)
    owner=User.objects.get(id=request.user.id)
    created=None
    f=None
    status=None

    try:
      f=Vote.objects.get(owner=owner,link=l)
      created=False
    except ObjectDoesNotExist:
      f=Vote.objects.create(owner=owner,link=l,direction=direction)
      created=True

    if created==False:
       if str(f.direction) != direction:
          if direction == "-1":
             l.total_votes=l.total_votes-2
             status="icon-remove:icon-chevron-up:%s" % l.total_votes
          elif direction == "1":
             l.total_votes=l.total_votes+2
             status="icon-chevron-down:icon-remove:%s" % l.total_votes

          f.direction = direction
          f.save()
          l.save()
       else:
          f.delete()
          if direction == "-1":
             l.total_votes=l.total_votes+1
          elif direction == "1":
             l.total_votes=l.total_votes-1
          status="icon-chevron-down:icon-chevron-up:%s" % l.total_votes
          l.save()
    elif created==True:
       if direction == "-1":
          l.total_votes=l.total_votes-1
          status="icon-remove:icon-chevron-up:%s" % l.total_votes
       elif direction == "1":
          l.total_votes=l.total_votes+1
          status="icon-chevron-down:icon-remove:%s" % l.total_votes
       l.save()


    return simplejson.dumps({'message':'%s:%s' % (status,l.id) })
