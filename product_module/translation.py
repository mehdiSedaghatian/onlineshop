from modeltranslation.translator import TranslationOptions, register

from product_module.models import Product, ProductCategory, ProductBrand


@register(Product)
class ProductTranslationOption(TranslationOptions):
    fields = ['title', 'short_description', 'description']


@register(ProductCategory)
class ProductCategoryTranslationOption(TranslationOptions):
    fields = ['title']


@register(ProductBrand)
class ProductBrandTranslationOption(TranslationOptions):
    fields = ['title']
