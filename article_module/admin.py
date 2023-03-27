from django.contrib import admin
from django.http import HttpRequest

from .models import ArticleCategory, Article, ArticleComment ,ArticleVisit


# Register your models here.
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'parent', 'is_active']
    list_editable = ['url_title', 'parent', 'is_active']


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'is_active', 'author']
    list_editable = ['is_active']

    def save_model(self, request: HttpRequest, obj: Article, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'create_date', 'parent']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleVisit)
admin.site.register(ArticleCategory, ArticleCategoryAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
