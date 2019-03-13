from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html


from .models import Post, Category, Tag


# Register your models here.
@admin.register(Category)             
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'is_nav', 'created_time')
    fields = ('name', 'status', 'is_nav')    # fields: 控制页面上要展示的字段

    
    def __str__(self):
        return self.name

    def save_model(self, request, obj, form, change):
        obj.owner = request.user     # 通过给obj.owner赋值，达到自动设置owner 目的。
        return super(CategoryAdmin, self).save_model(request, obj, form, change)
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


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
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

    fields = (
        ('category', 'title'),
        'desc',
        'status',
        'content',
        'tag',
    )

    def operator(self, obj):
        return fromat_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_post_change', args=(obj.id, ))
        )
    operator.short_description = '操作'


    def save_model(self, request, obj, form, change):
        obj,owner = request.user
        return super(PostAdmin, self).save_model(request, obj, form, change)
