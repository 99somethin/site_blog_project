from django.contrib import admin
from .models import PostModel, CommentModel, TagsModel

# Register your models here.
@admin.register(PostModel)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'slug', 'author', 'publish', 'status', 'get_tags']
    list_filter = ['status', 'created', 'publish', 'author']
    list_display_links = ['id', 'title', 'slug']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

    def get_tags(self, obj):
        return '\n'.join([item.name for item in obj.tags.all()])
    get_tags.short_description = 'Теги'



@admin.register(CommentModel)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'created', 'active', 'post_id']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']


@admin.register(TagsModel)
class TagsAdmin(admin.ModelAdmin):
    fields = ['name']
    list_display = ['name', 'slug']
