from modeltranslation.translator import register, TranslationOptions, translator

from main.models import News, Category


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('title', 'body')



@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name',)