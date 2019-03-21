from django.shortcuts import render
from django.shortcuts import  get_object_or_404
from django.views.generic import DetailView, ListView
from django.db.models import Q 

from blog.models import Post, Tag, Category
from comment.forms import CommentForm
from comment.models import Comment
# Create your views here.
def post_list(request, category_id=None, tag_id=None):
    tag = None
    category = None

    '''
    if tag_id:
        try :
            tag = Tag.objects.get(id=tag_id)
        except Tag.DoesNotExist:
            post_list = []
        else:
            post_list = tag.post_set.filter(status=Post.STATUS_NORMAL)
    else:
        post_list = Post.objects.filter(status=Post.STATUS_NORMAL)
        if category_id:
            try:
                category = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                category = None
            else:
                post_list = post_list.Filter(category_id=category_id)

    context = {
        'category':category,
        'tag':tag,
        'post_list':post_list,
    }
    return render(request, 'blog/list.html', context=context)
    '''

    '''
    如果查询到不存在的对象，需要通过try...except...来捕获并处理异常，避免当数据不存在时出现错误
    tag与post是多对多关系，因此需要先获取tag对象，接着通过该对象来获取对应的文章列表。
    '''
    if tag_id:
        post_list, tag = Post.get_by_tag(tag_id)
    elif category_id:
        post_list, category = Post.get_by_category(category_id)
    else:
        post_list = Post.latest_posts()


    from config.models import SideBar
    context = {
        'category':category,
        'tag': tag,
        'post_list': post_list,
        'sidebars': SideBar.get_all(),
    }
    context.update(Category.get_navs())
    return render(request, 'blog/list.html', context=context)


def post_detail(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        post = None
    return render(request, 'blog/detail.html', context={'post':post})

    '''
    介绍render（）方法：
    render(request, template_name, content=None, content_type=None, status=None, using=None)

    request: 封装了HTTP请求的request对象
    template_name: 模板名称，可以像前面的代码那样带上路径
    context: 字典数据，它会传递到模板中
    content_type: 页面编码类型，默认值是text/html
    status: 状态码，默认值是200
    using： 使用哪种模板引擎解析，这可以在settings中配置，默认使用Django自带模板
    '''

class CommonViewMixin:    
    def get_context_data(self, **kwargs):
        from config.models import SideBar
        context = super().get_context_data(**kwargs)
        context.update({
            'sidebars': SideBar.get_all(),
        })
        context.update(Category.get_navs())
        return context



class IndexView(CommonViewMixin, ListView):
    queryset = Post.latest_posts()
    paginate_by = 5
    context_object_name = 'post_list'
    template_name = 'blog/list.html'


class PostDetailView(CommonViewMixin, DetailView):
    
    '''
    model = Post
    template_name = 'blog/detail.html'
    '''
    queryset = Post.latest_posts()
    template_name = 'blog/detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'  # pk_url_kwarg = 'pk'

    
    '''
    DetailView 提供了如下如下属性和接口
    model 属性： 指定当前View要使用的Model
    queryset 属性： 跟Model一样，二选一。
                    设定基础的数据集，Model的设定没有过滤的功能，
                    可以通过queryset = Post.objects.filter(status=Post.STATUS_NORMAL)进行过滤
    template_name 属性： 模板名称
    get_queryset 接口： 根据URL参数，从queryset上获取到对应的实例
    get_context_data 接口: 获取渲染到模板中的所有上下午，如果有新增数据需要传递到模板中，
                           可以重写该方法来完成
    '''

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'comment_form': CommentForm,
            'comment_list': Comment.get_by_target(self.request.path),
        })
        return context


class PostListView(ListView):
    queryset = Post.latest_posts()
    paginate_by = 1
    context_object_name = 'post_list'  # 如果不设置此项，在模板中需要使用 object_list 变量
    template_name = 'blog/list.html'



class CategoryView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_id= self.kwargs.get('category_id')
        category = get_object_or_404(Category, pk=category_id)
        context.update({
            'category': category,
        })
        return context

    def get_queryset(self):
        '''重写queryset, 根据分类过滤 '''
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        return queryset.filter(category_id=category_id)


class TagView(IndexView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag_id = self.kwargs.get('tag_id')
        tag = get_object_or_404(Tag, pk=tag_id)
        context.update({
            'tag': tag,
        })
        return context

    def get_queryset(self):
        '''重写queryset, 根据标签过滤'''

        queryset = super().get_queryset()
        tag_id = self.kwargs.get('tag_id')
        return queryset.filter(tag__id=tag_id)

    '''
    get_object_or_404: 一个快捷方式，用来获取一个对象的实例。
                       如果获取到，就返回实例对象；如果不存在，直接抛出404错误
    tag_id = self.kwargs.get('tag_id')里面，self.kwargs 中的数据其实是URL定义中拿到的
    '''

class SearchView(IndexView):
    def get_context_data(self):
        context = super().get_context_data()
        context.update({
            'keyword': self.request.GET.get('keyword', '')
        })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        keyword = self.request.GET.get('keyword')
        if not keyword:
            return queryset
        return queryset.filter(Q(title__icontains=keyword) | Q(desc__icontains=keyword))


class AuthorView(IndexView):
    def get_queryset(self):
        queryset = super().get_queryset()
        author_id = self.kwargs.get('owner_id')
        return queryset.filter(owner_id=author_id)


