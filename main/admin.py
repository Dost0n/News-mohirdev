from django.contrib import admin
from main.models import Category, News, Contact, Comment


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug','publish_time', 'status']
    list_filter =  ['create_time','publish_time', 'status']
    prepopulated_fields = {"slug" : ('title',)}
    date_hierarchy = "publish_time"
    search_fields = ['title', 'body']
    ordering = ['status', 'publish_time']
    
admin.site.register(Category)
admin.site.register(Contact)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display  = ['user', 'news', 'created_time']
    list_filter   = ['user', 'news', 'created_time']
    search_fields = [ 'user','news', 'created_time']
    actions       = ['disbale_comments', 'enable_comments']
    
    def disbale_comments(self, request, queryset):
        queryset.update(active = False)
    
    def enable_comments(self, request, queryset):
        queryset.update(active = True)