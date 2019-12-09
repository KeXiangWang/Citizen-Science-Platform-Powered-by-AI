from haystack import indexes

# 修改此处，为你自己的model
from .models import ProjectInfo


# 修改此处，类名为模型类的名称+Index，比如模型类为GoodsInfo,则这里类名为GoodsInfoIndex
class ProjectInfoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)      # use_template说明搜索字段使用模板文件

    def get_model(self):
        # 修改此处，为你自己的model
        return ProjectInfo

    def index_queryset(self, using=None):
        return self.get_model().objects.all()