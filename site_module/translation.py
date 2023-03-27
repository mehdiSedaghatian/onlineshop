from modeltranslation.translator import TranslationOptions, register

from site_module.models import Slider, SiteSetting, FooterLinkBox, FooterLink


@register(Slider)
class SliderTranslationOption(TranslationOptions):
    fields = ['title', 'description', 'url_title']


@register(SiteSetting)
class SiteSettingTranslationOption(TranslationOptions):
    fields = ['copyright', 'about_us_text']


@register(FooterLinkBox)
class FooterLinkBoxTranslationOption(TranslationOptions):
    fields = ['title']


@register(FooterLink)
class FooterLinkTranslationOption(TranslationOptions):
    fields = ['title']
