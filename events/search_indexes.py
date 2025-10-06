from haystack import indexes
from .models import Event

class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)  
    title = indexes.CharField(model_attr='title')
    status = indexes.CharField(model_attr='status')
    category = indexes.CharField(model_attr='category')
    location = indexes.CharField(model_attr='location')
    date = indexes.DateField(model_attr='date')
    price = indexes.DecimalField(model_attr='price')

    def get_model(self):
        return Event  # Link this index to the Event model

    def index_queryset(self, using=None):
        return self.get_model().objects.all()  # Index all events
