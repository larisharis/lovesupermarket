from haystack import indexes
from models import Link
from tagging.models import Tag

class LinkIndex(indexes.RealTimeSearchIndex, indexes.Indexable):
   text = indexes.CharField(document=True, use_template=True)
   creation = indexes.DateField(model_attr='creation')
   title = indexes.CharField(model_attr='title')
   total_votes = indexes.IntegerField(model_attr='total_votes')
   tags = indexes.MultiValueField()
   free = indexes.CharField(model_attr='free')

   def get_model(self):
       return Link

   def index_queryset(self):
       return self.get_model().objects.all()

   def prepare(self, object):
       self.prepared_data = super(LinkIndex, self).prepare(object)
       self.prepared_data['tags'] = [tag.name for tag in Tag.objects.get_for_object(object)]

       return self.prepared_data
