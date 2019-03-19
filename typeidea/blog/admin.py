from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .adminforms import PostAdminForm


from .models import Post, Category, Tag
from typeidea.custom_site import custom_site


# Register your models here.
class CategoryOwnerFilter(admin.SimpleListFilter):
    '''自定义过滤器展示当前用户分类'''

    title = '分类过滤器'        # title 用于展示标题
    parameter_name = 'owner_category'    # parameter_name ：查询时URL参数的名字

    def lookups(self, request, model_admin):
        return Category.objects.filter(owner=request.user).values_list('id','name')
        '''
        lookups: 返回要展示的内容和查询用的id（就是Query用的）
        '''

    def queryset(self, request, queryset):
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.valur())
        return queryset
        '''
        queryset:根据URL Query的内容返回列表页数据。
                 比如如果URL最后的Query是？owner_category=1，那么这里拿到的self.value()就是1，
                 此时会根据1来过滤QuerySet。
                 这里的QuerySet是列表页所有展示数据的合集，即post的数据集。
        编完后，只需修改list_filter为：
            list_filter = [CategoryOwnerFilter]
            这样就能让用户在侧边栏的过滤器中只看到自己创建的分类了
        '''

@admin.register(Category)             
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav')    # fields: 控制页面上要展示的字段

    
    def __str__(self):
        return self.name

    def save_model(self, request, obj, form, change):
        obj.owner = request.user     # 通过给obj.owner赋值，达到自动设置owner 目的。
        return super().save_model(request, obj, form, change)
        '''
        request: 当前请求
        request.user: 当前已经登录的用户；如果未登录，则拿到的是匿名用户
        obj: 当前要保存的对象
        form: 页面提交过来的表单之后的对象
        change： 用于标志本次保持的数据是新增还是更新
        '''


    # 没有修饰符时，需要： 
    # admin.site.register(Category, CategoryAdmin)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_time')
    fields = ('name', 'status')

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


@admin.register(Post, )
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = [
        'title', 'category', 'status',
        'created_time', 'operator'
    ]                                     # 配置列表页面要展示的字段
    list_display_links = []               # 配置可以作为连接的字段，点击即可进入编辑页面

    list_filter = ['category', ]          # 配置页面过滤器
    search_fields = ['title', 'category__name'] # 配置搜索字段

    actions_on_top = True                 # 动作相关配置，是否展示在顶部
    actions_on_bottom = True              # 动作相关配置，是否展示在底部
    


    # 编辑页面
    save_on_top = True                    # 保存、编辑、编辑并新建按钮是否在顶部展示
    '''
    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
        'owner',           # 因为BUG而添加：'User' object is not iterable
    )
    '''
    fieldsets = (
        ('基础配置', {
            'description': '基础配置描述',
            'fields':(
                ('title', 'category'),
                'status',
            ),
        }),
        ('内容',{
            'fields':(
                'desc',
                'content',
            ),
        }),
        ('额外信息', {
            'classes':('collapse',),
            'fields':('tag',),
        })
    )
    '''
    fieldsets = (
        (名称,{内容}),
        (名称,{内容}),
    )
    dict的key可以是：'fields'、'description'和'classes'
        fields: 控制展示哪些元素，也可以给元素排序并组合元素的位置
        classes: 给要配置的板块加上CSS属性
    '''

    def operator(self, obj):
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id, ))
        )
        operator.short_description = '操作'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)

    def get_queryset(self, request):
        qs = super(PostAdmin, self).get_queryset(request)
        return qs.filter(owner=request.user)

class PostInline(admin.TabularInline): # stackedInline 样式不同
    fields = ('title', 'desc')
    extra = 1 # 控制额外多几个
    model = Post


class CategoryAdmin(admin.ModelAdmin):
    inlines = [PostInline, ]
