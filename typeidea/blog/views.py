from django.shortcuts import render

from .models import Post, Tag, Category

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

    context = {
        'category':category,
        'tag': tag,
        'post_list': post_list,
    }
    #context.update(Category.get_navs())
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

