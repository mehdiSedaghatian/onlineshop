from modeltranslation.translator import TranslationOptions, register

from article_module.models import Article


@register(Article)
class ArticleTranslationOption(TranslationOptions):
    fields = ['title', 'short_description', 'text']
