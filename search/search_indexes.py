from haystack import indexes
from micro_blog.models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name="search/post_text.txt")
    title = indexes.CharField(model_attr='title')
    auther = indexes.CharField()
    title_auto = indexes.EdgeNgramField(model_attr='title')
    post_url = indexes.CharField()
    created_on = indexes.CharField(model_attr='created_on')

    def get_model(self):
        return Post

    def prepare_post_url(self, obj):
        return obj.get_url

    def prepare_auther(self, obj):
        return obj.user.username

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
